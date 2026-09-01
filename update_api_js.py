# -*- coding: utf-8 -*-
with open("frontend/src/services/api.js", "w", encoding="utf-8") as f:
    f.write("""import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

export const fetchHealth = async () => (await apiClient.get('/health')).data;
export const loginUser = async (credentials) => (await apiClient.post('/login', credentials)).data;
export const fetchDashboard = async () => (await apiClient.get('/dashboard')).data;
export const fetchIndiaRisk = async () => (await apiClient.get('/dashboard/india-risk')).data;
export const fetchStateRisk = async (state) => (await apiClient.get(`/dashboard/state/${encodeURIComponent(state)}`)).data;
export const fetchDistrictRisk = async (district) => (await apiClient.get(`/dashboard/district/${encodeURIComponent(district)}`)).data;

export const fetchAnimals = async (params = {}) => (await apiClient.get('/animals', { params })).data;
export const fetchAnimalDetail = async (id) => (await apiClient.get(`/animals/${id}`)).data;
export const registerAnimal = async (payload) => (await apiClient.post('/animals/register', payload)).data;
export const fetchSensorData = async (id) => (await apiClient.get(`/sensor-data/${id}`)).data;
export const fetchAnimalPrediction = async (id) => (await apiClient.get(`/predictions/${id}`)).data;
export const predictRisk = async (payload) => (await apiClient.post('/predict', payload)).data;
export const fetchModelPerformance = async () => (await apiClient.get('/model-performance')).data;
""")

print("Updated frontend/src/services/api.js with India risk methods.")
