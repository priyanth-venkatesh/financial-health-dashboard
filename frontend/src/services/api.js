import axios from "axios";

const API = axios.create({
  baseURL: "https://finance-backend-lmao.onrender.com",
});

export default API;
