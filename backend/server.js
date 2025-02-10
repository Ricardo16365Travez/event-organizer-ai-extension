const express = require("express");
const cors = require("cors");
require("dotenv").config();

const app = express();
app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.json({ message: "API funcionando correctamente" });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Servidor en http://localhost:${PORT}`);
});

const aiRoutes = require("./routes/ai");
app.use("/api/ai", aiRoutes);
