import React, { useState } from "react";
import ChatForm from "./components/chat/ChatForm";
import ResponseDisplay from "./components/chat/ResponseDisplay";
import { sendChatRequest } from "./api/apiClient";
import "./index.css";

export default function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (payload) => {
    setIsLoading(true);
    setError("");
    setData(null);

    try {
      const result = await sendChatRequest(payload);
      setData(result);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <h1>Walled Garden AI</h1>
        <p className="subtitle">
          Age-aware AI safety demo with RAG and guardrails.
        </p>

        <ChatForm onSubmit={handleSubmit} isLoading={isLoading} />
        <ResponseDisplay data={data} error={error} isLoading={isLoading} />
      </div>
    </div>
  );
}