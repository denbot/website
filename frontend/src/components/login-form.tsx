'use client';

import { AuthStatus } from '@/models/auth-flow-response.model';
import { login, loginOtp } from '@/services/authentication';
import { Stack, TextField, Button, Typography } from '@mui/material';
import { matchIsValidTel, MuiTelInput } from 'mui-tel-input';
import { useRouter, useSearchParams } from 'next/navigation';
import { useRef, useState } from 'react';

const VERIFICATION_CODE_LENGTH = 6;
const RESEND_TIMER_LENGTH = 30;

export default function LoginForm() {
  const [status, setStatus] = useState<AuthStatus>('initial');
  const [phoneNumber, setPhoneNumber] = useState<string>('');
  const [phoneNumberError, setPhoneNumberError] = useState<boolean>(false);
  const [otp, setOtp] = useState<string>('');
  const [resendTimer, setResendTimer] = useState<number>(0);
  const [warningText, setWarningText] = useState<string>('');

  const timerRef = useRef<ReturnType<typeof setInterval>>(null);
  const router = useRouter();
  const searchParams = useSearchParams();

  const startResendTimer = () => {
    setResendTimer(RESEND_TIMER_LENGTH);
    timerRef.current = setInterval(() => {
      setResendTimer((timer: number): number => {
        if (timer < 1) {
          clearInterval(timerRef.current!);
          return 0;
        }
        return timer - 1;
      });
    }, 1000);
  };

  const submit = () => {
    if (status == 'initial') {
      submitPhoneNumber();
    } else if (status == 'pending') {
      submitOtp(otp);
    }
  };

  const submitPhoneNumber = async () => {
    const status: AuthStatus = await login(phoneNumber);
    setStatus(status);
    if (status == 'pending') {
      startResendTimer();
    }
  };

  const submitOtp = async (code: string) => {
    setWarningText('');
    const status: AuthStatus = await loginOtp(phoneNumber, code);
    if (status == 'approved') {
      handleRedirect();
    }
    setStatus(status);
    setWarningText(getWarningText());
  };

  const handleRedirect = () => {
    const nextUrl = searchParams?.get('next') ?? '/';
    router.replace(nextUrl);
  };

  const isOtpValid = (code: string): boolean => {
    return code.length == VERIFICATION_CODE_LENGTH;
  };

  const updateOTP = (code: string) => {
    if (isOtpValid(code)) {
      submitOtp(code);
    }
    setOtp(code);
  };

  const updatePhoneNumber = (number: string, allowNewError?: boolean) => {
    const hasError = !matchIsValidTel(number);
    if (hasError != phoneNumberError) {
      if (allowNewError || !hasError) {
        setPhoneNumberError(hasError);
      }
    }
    setPhoneNumber(number);
  };

  const isSubmitButtonDisabled = (): boolean => {
    if (status == 'initial') {
      return !matchIsValidTel(phoneNumber);
    } else if (status == 'pending') {
      return !isOtpValid(otp);
    }
    return true;
  };

  const getWarningText = () => {
    switch (status) {
      case 'initial':
      case 'approved':
      case 'error':
        return '';
      case 'pending':
        return 'Verification code incorrect.';
      case 'canceled':
      case 'max_attempts_reached':
      case 'deleted':
      case 'failed':
      case 'expired':
        return 'Verification code no longer valid. Request a new code.';
    }
  };

  return (
    <Stack spacing={2}>
      <MuiTelInput
        id="phone_number"
        label="Phone Number"
        placeholder="Enter phone number"
        error={phoneNumberError}
        helperText={phoneNumberError && 'Invalid phone number'}
        value={phoneNumber}
        onChange={(value) => updatePhoneNumber(value)}
        onBlur={() => updatePhoneNumber(phoneNumber, true)}
        disabled={status != 'initial'}
        fullWidth
        forceCallingCode
        defaultCountry="US"
        disableDropdown
      />
      {status == 'pending' && (
        <TextField
          id="otp"
          label="Verification Code"
          placeholder="Enter 6-digit code"
          type="number"
          value={otp}
          onChange={(event) => updateOTP(event.target.value)}
        />
      )}
      {warningText && (
        <Typography
          variant="body1"
          color="warning"
        >
          {warningText}
        </Typography>
      )}
      {status == 'error' && (
        <Typography
          variant="body1"
          color="error"
        >
          Oops! something went wrong
        </Typography>
      )}
      <Button
        onClick={submit}
        disabled={isSubmitButtonDisabled()}
        variant="contained"
        size="large"
      >
        Submit
      </Button>
      {status != 'initial' && (
        <Button
          onClick={submitPhoneNumber}
          variant="contained"
          size="large"
          disabled={resendTimer > 0}
        >
          Resend Code
          {resendTimer > 0 && <span> ({resendTimer}s)</span>}
        </Button>
      )}
    </Stack>
  );
}
