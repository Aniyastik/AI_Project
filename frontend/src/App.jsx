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
    <>
      <div className="zen-orbs-wrapper">
        <div className="organic-orb orb-sage"></div>
        <div className="organic-orb orb-blue"></div>
      </div>
      <div className="app-wrapper">
        <div className="container">
          <h1>Minor-Guard</h1>
          <p className="subtitle">
            Structural Protection UI • Secure AI Interface
          </p>

          <ChatForm onSubmit={handleSubmit} isLoading={isLoading} />
          <ResponseDisplay data={data} error={error} isLoading={isLoading} />
        </div>
      </div>
    </>
  );
}