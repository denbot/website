'use client';

import { login, loginOtp } from '@/services/authentication';
import { ReactElement, useState } from 'react';
import 'react-phone-number-input/style.css';
import { MuiTelInput, matchIsValidTel } from 'mui-tel-input';
import { Box, Button, Container, Paper, Stack, TextField } from '@mui/material';

const VERIFICATION_CODE_LENGTH = 6;

export function LoginButton(): ReactElement {
  const [stage, setStage] = useState<string>('initial');
  const [phoneNumber, setPhoneNumber] = useState<string>('');
  const [phoneNumberError, setPhoneNumberError] = useState<boolean>(false);
  const [otp, setOtp] = useState<string>('');

  const submit = () => {
    if (stage == 'initial') {
      submitPhoneNumber();
    } else if (stage == 'otp') {
      submitOtp(otp);
    }
  };

  const submitPhoneNumber = async () => {
    const loginResult: boolean = await login(phoneNumber);
    setStage(loginResult ? 'otp' : 'failure');
  };

  const submitOtp = async (code: string) => {
    const otpResult = await loginOtp(phoneNumber, code);
    setStage(otpResult ? 'accepted' : 'failure');
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
      if (!hasError || (hasError && allowNewError)) {
        setPhoneNumberError(hasError);
      }
    }
    setPhoneNumber(number);
  };

  const isSubmitButtonDisabled = (): boolean => {
    if (stage == 'initial') {
      return !phoneNumber || phoneNumberError;
    } else if (stage == 'otp') {
      return isOtpValid(otp);
    }
    return true;
  };

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      height="100vh"
    >
      <Container maxWidth="xs">
        <Paper
          elevation={3}
          sx={{ p: 3 }}
        >
          <Stack spacing={2}>
            <MuiTelInput
              id="phone_number"
              label="Phone Number"
              error={phoneNumberError}
              helperText={phoneNumberError && 'ERROR!'}
              value={phoneNumber}
              onChange={(value) => updatePhoneNumber(value ?? '')}
              onBlur={(value) => updatePhoneNumber(phoneNumber, true)}
              disabled={stage != 'initial'}
              fullWidth
              forceCallingCode
              defaultCountry="US"
              disableDropdown
            />
            {stage == 'otp' && (
              <TextField
                id="otp"
                label="Enter One-time Code"
                type="number"
                value={otp}
                onChange={(event) => updateOTP(event.target.value)}
              />
            )}
            {(stage == 'initial' || stage == 'otp') && (
              <Button
                onClick={submit}
                disabled={isSubmitButtonDisabled()}
                variant="contained"
                size="large"
              >
                Submit
              </Button>
            )}
            {stage == 'accepted' && 'You are logged in!'}
          </Stack>
        </Paper>
      </Container>
    </Box>
  );
}

export default LoginButton;
