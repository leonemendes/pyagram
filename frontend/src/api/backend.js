// src/api/backend.js
import axios from 'axios';
const BASE_URL = 'http://localhost:8000';

export async function runWorkflow(workflow, inputs) {
    const { data } = await axios.post(`${BASE_URL}/run`, { workflow, inputs });
    return data.result;
}
