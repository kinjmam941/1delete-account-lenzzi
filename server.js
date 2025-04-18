const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const fetch = require("node-fetch");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());

const SHOPIFY_STORE_URL = process.env.SHOPIFY_STORE_URL;
const SHOPIFY_ACCESS_TOKEN = process.env.SHOPIFY_ACCESS_TOKEN;

app.post("/delete-customer", async (req, res) => {
  const { customer_id } = req.body;
  if (!customer_id) {
    return res.status(400).json({ message: "Missing customer_id" });
  }

  const url = `${SHOPIFY_STORE_URL}/admin/api/2024-04/customers/${customer_id}.json`;

  try {
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
      },
    });

    if (!response.ok) {
      const error = await response.text();
      return res.status(response.status).json({ message: error });
    }

    return res.status(200).json({ message: "Customer deleted successfully" });
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});