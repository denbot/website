'use client';

import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { MuiTelInput, matchIsValidTel } from 'mui-tel-input';
import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useRef, useState } from 'react';

import { AuthStatus } from '@/models/auth-flow-response.model';
import { login, loginOtp } from '@/services/authentication';

import ThemedLogo from './themed-logo';

const VERIFICATION_CODE_LENGTH = 6;
const RESEND_TIMER_LENGTH = 30;

export default function LoginForm() {
  const [status, setStatus] = useState<AuthStatus>('initial');
  const [phoneNumber, setPhoneNumber] = useState<string>('');
  const [phoneNumberError, setPhoneNumberError] = useState<boolean>(false);
  const [otp, setOtp] = useState<string>('');
  const [resendTimer, setResendTimer] = useState<number>(0);
  const [warningText, setWarningText] = useState<string>('');
  const [showOtp, setShowOtp] = useState<boolean>(false);

  const timerRef = useRef<ReturnType<typeof setInterval>>(null);
  const router = useRouter();
  const searchParams = useSearchParams();

  const phoneNumberRef = useRef<HTMLInputElement>(null);
  const otpRef = useRef<HTMLInputElement>(null);

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
    } else {
      submitOtp(otp);
    }
  };

  const submitPhoneNumber = async () => {
    const status: AuthStatus = await login(phoneNumber);
    setStatus(status);
    if (status != 'error') {
      setShowOtp(true);
      startResendTimer();
    }
  };

  const submitOtp = async (code: string) => {
    setWarningText('');
    const status: AuthStatus = await loginOtp(phoneNumber, code);
    setStatus(status);
    setShowOtp(status != 'error' && status != 'too_many_attempts');
    setWarningText(getWarningText());
    if (status == 'approved') {
      handleRedirect();
    }
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
    } else if (status != 'error') {
      return !isOtpValid(otp);
    }
    return true;
  };

  const getWarningText = () => {
    switch (status) {
      case 'initial':
      case 'created':
      case 'approved':
      case 'error':
        return '';
      case 'failed':
        return 'Verification code incorrect.';
      case 'expired':
        return 'Verification code no longer valid. New code has been requested.';
      case 'too_many_attempts':
        return 'Too many recent failed login attempts. Try again later.';
    }
  };

  const handleSubmitOnEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !isSubmitButtonDisabled()) {
      submit();
    }
  };

  // focus on phone number input when page loads
  useEffect(() => {
    if (phoneNumberRef.current) {
      phoneNumberRef.current.focus();
    }
  }, []);

  // focus on otp input when field loads
  useEffect(() => {
    if (showOtp && otpRef.current) {
      otpRef.current.focus();
    }
  }, [showOtp]);

  return (
    <Stack spacing={2}>
      <ThemedLogo />
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
        inputRef={phoneNumberRef}
        onKeyDown={handleSubmitOnEnter}
      />
      {showOtp && (
        <TextField
          id="otp"
          label="Verification Code"
          placeholder="Enter 6-digit code"
          type="number"
          value={otp}
          onChange={(event) => updateOTP(event.target.value)}
          inputRef={otpRef}
          onKeyDown={handleSubmitOnEnter}
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
      {(showOtp || status == 'initial') && (
        <Button
          onClick={submit}
          disabled={isSubmitButtonDisabled()}
          variant="contained"
          size="large"
        >
          Submit
        </Button>
      )}
      {showOtp && (
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
