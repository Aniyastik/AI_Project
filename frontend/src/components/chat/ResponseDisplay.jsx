import React from "react";

export default function ResponseDisplay({ data, error, isLoading }) {
  if (isLoading) {
    return (
      <div className="card loading-container">
        <div className="loading-pulse">Reflecting...</div>
      </div>
    );
  }

  if (error) {
    return <div className="card error">{error}</div>;
  }

  if (!data) return null;

  return (
    <div className="card response-card">
      <div className="meta">
        <span><strong>System</strong> {data.system}</span>
        <span><strong>Age</strong> {data.age}</span>
        {data.retrieved_topic && (
          <span><strong>Topic</strong> {data.retrieved_topic}</span>
        )}
      </div>

      <div className="response-text">
        {data.response}
      </div>
    </div>
  );
}