import LoginForm from '@/components/login-form';
import { Box, Container, Paper } from '@mui/material';

export default function LoginPage() {
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
          <LoginForm />
        </Paper>
      </Container>
    </Box>
  );
}
