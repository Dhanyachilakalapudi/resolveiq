import { useEffect, useState } from "react";
import api from "./api";
import "./App.css";

function App() {

  const [exceptions, setExceptions] = useState([]);
  const [selected, setSelected] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadExceptions();
  }, []);

  async function loadExceptions() {
    try {
      const response = await api.get("/exceptions");

      console.log("EXCEPTIONS:", response.data);

      setExceptions(response.data);

      // Keep selected exception synchronized with database state.
      if (selected) {
        const updated = response.data.find(
          (item) => item.exception_id === selected.exception_id
        );

        if (updated) {
          setSelected(updated);
        }
      }

    } catch (error) {
      console.error("EXCEPTIONS ERROR:", error);
    }
  }

  async function analyzeException(exceptionId) {

    setLoading(true);

    try {

      const response = await api.post(
        `/resolution/${exceptionId}`
      );

      console.log("RESOLUTION:", response.data);

      setAnalysis(response.data);

      // Refresh queue so backend status is immediately visible.
      await loadExceptions();

    } catch (error) {

      console.error("RESOLUTION ERROR:", error);

      setAnalysis({
        analysis: "AI analysis is currently unavailable.",
        recommended_action:
          "Review the exception manually before taking action.",
        confidence: 0,
        threshold: 0.90,
        decision: "HUMAN REVIEW",
        auto_resolve: false,
        requires_human_review: true,
        confidence_reason:
          "Automatic resolution is unavailable because AI analysis failed. Human review is required."
      });

    } finally {

      setLoading(false);

    }
  }

  async function approveException(exceptionId) {

    try {

      await api.post(
        `/workflow/${exceptionId}/approve`
      );

      await loadExceptions();

      setAnalysis(null);

    } catch (error) {

      console.error("APPROVE ERROR:", error);

    }
  }

  async function rejectException(exceptionId) {

    try {

      await api.post(
        `/workflow/${exceptionId}/reject`
      );

      await loadExceptions();

      setAnalysis(null);

    } catch (error) {

      console.error("REJECT ERROR:", error);

    }
  }

  const thresholdPercent = analysis?.threshold
    ? (analysis.threshold * 100).toFixed(0)
    : "90";

  const confidencePercent = analysis
    ? ((analysis.confidence || 0) * 100).toFixed(0)
    : "0";

  const isAutoResolved =
    analysis?.decision === "AUTO-RESOLVE";

  return (

    <div className="app">

      <header>

        <h1>ResolveIQ</h1>

        <p>
          AI-Assisted Exception Resolution Workbench
        </p>

      </header>

      <main>

        <section className="queue">

          <h2>Exception Queue</h2>

          {exceptions.map((item) => (

            <button
              className="exception-card"
              key={item.exception_id}
              onClick={() => {
                setSelected(item);
                setAnalysis(null);
              }}
            >

              <strong>
                {item.exception_id}
              </strong>

              <span>
                {item.exception_type}
              </span>

              <span>
                {item.severity}
              </span>

              <span>
                {item.status}
              </span>

            </button>

          ))}

        </section>

        <section className="details">

          {selected ? (

            <>

              <h2>
                {selected.exception_id}
              </h2>

              <p>
                <strong>Invoice:</strong>{" "}
                {selected.invoice_id}
              </p>

              <p>
                <strong>Vendor:</strong>{" "}
                {selected.vendor}
              </p>

              <p>
                <strong>Type:</strong>{" "}
                {selected.exception_type}
              </p>

              <p>
                <strong>Severity:</strong>{" "}
                {selected.severity}
              </p>

              <p>
                <strong>Description:</strong>{" "}
                {selected.description}
              </p>

              <p>
                <strong>Expected:</strong>{" "}
                {selected.expected_value ?? "N/A"}
              </p>

              <p>
                <strong>Actual:</strong>{" "}
                {selected.actual_value ?? "N/A"}
              </p>

              <p>
                <strong>Difference:</strong>{" "}
                {selected.difference ?? "N/A"}
              </p>

              <p>
                <strong>Current Status:</strong>{" "}
                {selected.status}
              </p>

              <button
                className="analyze"
                onClick={() =>
                  analyzeException(selected.exception_id)
                }
                disabled={loading}
              >

                {loading
                  ? "Analyzing..."
                  : "Analyze Exception"}

              </button>

              {analysis && (

                <div className="analysis">

                  <h3>AI Analysis</h3>

                  <p>
                    {analysis.analysis}
                  </p>

                  <h3>Recommended Action</h3>

                  <p>
                    {analysis.recommended_action}
                  </p>

                  <h3>Confidence</h3>

                  <p>
                    <strong>
                      {confidencePercent}%
                    </strong>
                  </p>

                  <h3>Confidence Gate</h3>

                  <p>
                    {isAutoResolved
                      ? `✓ Above ${thresholdPercent}% threshold`
                      : `⚠ Below ${thresholdPercent}% threshold`}
                  </p>

                  <h3>System Decision</h3>

                  <p>
                    <strong>
                      {analysis.decision}
                    </strong>
                  </p>

                  <p>
                    {analysis.confidence_reason}
                  </p>

                  <h3>Status</h3>

                  <p>
                    <strong>
                      {analysis.status ||
                        (isAutoResolved
                          ? "RESOLVED"
                          : selected.status)}
                    </strong>
                  </p>

                  {analysis.requires_human_review && (

                    <div className="review">

                      <p>
                        <strong>
                          Human review is required.
                        </strong>
                      </p>

                      <button
                        onClick={() =>
                          approveException(
                            selected.exception_id
                          )
                        }
                      >
                        Approve
                      </button>

                      <button
                        onClick={() =>
                          rejectException(
                            selected.exception_id
                          )
                        }
                      >
                        Reject
                      </button>

                    </div>

                  )}

                  {isAutoResolved && (

                    <div className="review">

                      <p>
                        ✓ Exception automatically resolved
                        by the confidence gate.
                      </p>

                    </div>

                  )}

                </div>

              )}

            </>

          ) : (

            <p>
              Select an exception from the queue.
            </p>

          )}

        </section>

      </main>

    </div>

  );
}

export default App;
