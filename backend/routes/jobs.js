const express = require('express');
const router = express.Router();
const { db } = require('../server');

router.post('/', async (req, res) => {
  try {
    const { title, company, location, description } = req.body;
    const jobRef = await db.collection('jobs').add({ title, company, location, description });
    res.status(201).send({ id: jobRef.id });
  } catch (error) {
    res.status(500).send({ error: error.message });
  }
});

router.get('/', async (req, res) => {
  try {
    const jobs = [];
    const snapshot = await db.collection('jobs').get();
    snapshot.forEach(doc => jobs.push({ id: doc.id, ...doc.data() }));
    res.send(jobs);
  } catch (error) {
    res.status(500).send({ error: error.message });
  }
});

module.exports = router;
