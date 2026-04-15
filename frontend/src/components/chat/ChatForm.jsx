import { useState } from "react";

const SYSTEMS = ["Baseline", "RAG", "Guardrails", "Proposed"];

export default function ChatForm({ onSubmit, isLoading }) {
  const [prompt, setPrompt] = useState("");
  const [age, setAge] = useState(12);
  const [system, setSystem] = useState("Proposed");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    onSubmit({
      prompt: prompt.trim(),
      age: Number(age),
      system,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="card form-card">
      <label>
        Prompt
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Ask something..."
          rows={5}
        />
      </label>

      <div className="row">
        <label>
          Age
          <input
            type="number"
            min="5"
            max="99"
            value={age}
            onChange={(e) => setAge(e.target.value)}
          />
        </label>

        <label>
          System
          <select value={system} onChange={(e) => setSystem(e.target.value)}>
            {SYSTEMS.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>
      </div>

      <button type="submit" disabled={isLoading || !prompt.trim()}>
        {isLoading ? "Thinking..." : "Send"}
      </button>
    </form>
  );
}