const API_CONFIG = {
  PROTOCOL: 'http',
  BASEURL: 'localhost:8000',
};


// noinspection LongLine
const TEST_PROMPT = `
Write a Python script that generates a list of 100 random integers between 1 and 100000. The script should then calculate and print the mean, median, and standard deviation of these numbers. Ensure to include necessary imports and handle any potential errors.  print the list of numbers to the console as well as the results.
`

export {API_CONFIG, TEST_PROMPT};