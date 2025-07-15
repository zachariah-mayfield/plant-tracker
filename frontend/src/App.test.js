import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Plant Tracker heading', () => {
  render(<App />);
  const headingElement = screen.getByText(/Plant Tracker/i);
  expect(headingElement).toBeInTheDocument();
}); 