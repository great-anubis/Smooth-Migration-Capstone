const request = require("supertest");
const app     = require("../server");

describe("POST /recommendations", () => {
  it("responds with tasks array", async () => {
    const res = await request(app)
      .post("/recommendations")
      .send({ "What is your full name?":"Test User" });
    expect(res.statusCode).toBe(200);
    expect(Array.isArray(res.body.tasks)).toBe(true);
    expect(res.body.tasks.length).toBeGreaterThan(0);
  });
});
