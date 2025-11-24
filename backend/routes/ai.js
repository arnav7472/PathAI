const express = require('express');
const router = express.Router();
const { Configuration, OpenAIApi } = require('openai');

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

router.post('/generate-resume', async (req, res) => {
  try {
    const { skills, experience, education } = req.body;
    const prompt = `Create a professional resume for a job seeker with the following details:
      Skills: ${skills.join(', ')}
      Experience: ${experience}
      Education: ${education}
    `;
    const response = await openai.createCompletion({
      model: 'text-davinci-003',
      prompt,
      max_tokens: 500,
    });
    res.send({ resume: response.data.choices[0].text });
  } catch (error) {
    res.status(500).send({ error: error.message });
  }
});

module.exports = router;
