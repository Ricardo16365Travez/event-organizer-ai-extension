const express = require("express");
const router = express.Router();

router.post("/recommend-speakers", (req, res) => {
  const speakers = [
    { name: "Dr. Juan Pérez", expertise: "Inteligencia Artificial" },
    { name: "Dra. Ana Gómez", expertise: "Ciberseguridad" }
  ];
  res.json(speakers);
});

module.exports = router;
