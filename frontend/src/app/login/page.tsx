import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';

import LoginForm from '@/components/login-form';

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
