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
    } catch (error) {
      console.error("EXCEPTIONS ERROR:", error);
    }
  }

  async function analyzeException(exceptionId) {

    setLoading(true);

    try {

      const response = await api.post(`/resolution/${exceptionId}`);

      console.log("RESOLUTION:", response.data);

      setAnalysis(response.data);

    } catch (error) {

      console.error("RESOLUTION ERROR:", error);

      setAnalysis({
        analysis: "Unable to generate AI analysis.",
        recommended_action: "Please try again or send this exception for human review.",
        confidence: 0,
        decision: "REVIEW",
        requires_human_review: true
      });

    } finally {

      setLoading(false);

    }
  }

  async function approveException(exceptionId) {

    try {

      await api.post(`/workflow/${exceptionId}/approve`);

      await loadExceptions();

      setAnalysis(null);

    } catch (error) {

      console.error("APPROVE ERROR:", error);

    }
  }

  async function rejectException(exceptionId) {

    try {

      await api.post(`/workflow/${exceptionId}/reject`);

      await loadExceptions();

      setAnalysis(null);

    } catch (error) {

      console.error("REJECT ERROR:", error);

    }
  }

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
                {selected.expected_value}
              </p>

              <p>
                <strong>Actual:</strong>{" "}
                {selected.actual_value}
              </p>

              <p>
                <strong>Difference:</strong>{" "}
                {selected.difference}
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
                    {(analysis.confidence * 100).toFixed(0)}%
                  </p>

                  <h3>Decision</h3>

                  <p>
                    {analysis.decision}
                  </p>

                  <div>

                    <p>
                      Human approval workflow
                    </p>

                    <button
                      onClick={() =>
                        approveException(selected.exception_id)
                      }
                    >
                      Approve
                    </button>

                    <button
                      onClick={() =>
                        rejectException(selected.exception_id)
                      }
                    >
                      Reject
                    </button>

                  </div>

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


