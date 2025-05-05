const checklistMapping = require("../models/checklist_mapping.json");
const enrich = require("../server")._enrichTask; 

test("fallback 'general' for unmapped text", () => {
  const raw = { description:"Random unrelated stuff" };
  const out = enrich(raw);
  expect(out.api_trigger).toBe("general");
  expect(out.service).toBe("general");
});

