import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, AlertTriangle, Activity, FileText, Download, Clock, Server } from 'lucide-react';
import axios from 'axios';

const ErrorDetail = () => {
  const { errorId } = useParams();
  const [errorData, setErrorData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchErrorDetails();
  }, [errorId]);

  const fetchErrorDetails = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/errors/${errorId}`);
      setErrorData(response.data);
    } catch (error) {
      console.error('Error fetching error details:', error);
    } finally {
      setLoading(false);
    }
  };

  const downloadErrorData = async () => {
    try {
      const response = await axios.get(`/api/errors/${errorId}/download`);
      const dataStr = JSON.stringify(response.data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `error-${errorId}.json`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading data:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!errorData) {
    return (
      <div className="text-center py-8">
        <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Not Found</h2>
        <p className="text-gray-600 mb-4">The requested error could not be found.</p>
        <Link
          to="/dashboard"
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Back to Dashboard
        </Link>
      </div>
    );
  }

  const { error, traces, spans, logs, rca_report } = errorData;

  const tabs = [
    { id: 'overview', name: 'Overview', icon: AlertTriangle },
    { id: 'traces', name: 'Traces', icon: Activity, count: traces.length },
    { id: 'spans', name: 'Spans', icon: Server, count: spans.length },
    { id: 'logs', name: 'Logs', icon: FileText, count: logs.length },
    { id: 'rca', name: 'RCA Analysis', icon: Clock }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link
            to="/dashboard"
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <ArrowLeft className="h-6 w-6" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Error Details</h1>
            <p className="text-gray-600">ID: {errorId}</p>
          </div>
        </div>
        <button
          onClick={downloadErrorData}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
        >
          <Download className="h-4 w-4" />
          <span>Download JSON</span>
        </button>
      </div>

      {/* Error Summary */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Error Summary</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Environment</label>
            <p className="text-sm text-gray-900">{error.env || 'UNSET'}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Service</label>
            <p className="text-sm text-gray-900">{error.service}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">HTTP Code</label>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
              {error.http_code}
            </span>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Exception</label>
            <p className="text-sm text-gray-900">{error.exception}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Count</label>
            <p className="text-sm text-gray-900">{error.count}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Time Window</label>
            <p className="text-sm text-gray-900">
              {new Date(error.window_start).toLocaleString()} - {new Date(error.window_end).toLocaleString()}
            </p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.name}</span>
                  {tab.count !== undefined && (
                    <span className="bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full text-xs">
                      {tab.count}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        <div className="p-6">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <Activity className="h-5 w-5 text-blue-600" />
                    <span className="font-medium text-blue-900">Traces</span>
                  </div>
                  <p className="text-2xl font-bold text-blue-900 mt-2">{traces.length}</p>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <Server className="h-5 w-5 text-green-600" />
                    <span className="font-medium text-green-900">Spans</span>
                  </div>
                  <p className="text-2xl font-bold text-green-900 mt-2">{spans.length}</p>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <FileText className="h-5 w-5 text-purple-600" />
                    <span className="font-medium text-purple-900">Logs</span>
                  </div>
                  <p className="text-2xl font-bold text-purple-900 mt-2">{logs.length}</p>
                </div>
              </div>

              {rca_report && (
                <div className="bg-yellow-50 p-4 rounded-lg">
                  <h3 className="font-medium text-yellow-900 mb-2">RCA Analysis</h3>
                  <div className="prose prose-sm max-w-none">
                    <pre className="whitespace-pre-wrap text-sm text-yellow-800 bg-yellow-100 p-3 rounded">
                      {rca_report.analysis_summary}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Traces Tab */}
          {activeTab === 'traces' && (
            <div>
              {traces.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <Activity className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                  <p>No traces found for this error</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {traces.map((trace) => (
                    <div key={trace.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <Activity className="h-4 w-4 text-blue-600" />
                          <span className="font-mono text-sm">{trace.trace_id_hex}</span>
                        </div>
                        <span className="text-xs text-gray-500">
                          {new Date(trace.created_at).toLocaleString()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Spans Tab */}
          {activeTab === 'spans' && (
            <div>
              {spans.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <Server className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                  <p>No spans found for this error</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Operation
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Trace ID
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Duration
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Start Time
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {spans.map((span) => (
                        <tr key={span.id}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {span.operation_name}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">
                            {span.trace_id}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {span.duration}ms
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {span.start_time ? new Date(span.start_time).toLocaleString() : 'N/A'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {/* Logs Tab */}
          {activeTab === 'logs' && (
            <div>
              {logs.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                  <p>No logs found for this error</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {logs.map((log) => (
                    <div key={log.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-900">Trace: {log.trace_id}</span>
                        <span className="text-xs text-gray-500">
                          {new Date(log.created_at).toLocaleString()}
                        </span>
                      </div>
                      <pre className="text-sm text-gray-700 bg-gray-50 p-3 rounded overflow-x-auto">
                        {JSON.stringify(log.log_data, null, 2)}
                      </pre>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* RCA Analysis Tab */}
          {activeTab === 'rca' && (
            <div>
              {rca_report ? (
                <div className="space-y-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h3 className="font-medium text-blue-900 mb-2">Analysis Summary</h3>
                    <div className="prose prose-sm max-w-none">
                      <pre className="whitespace-pre-wrap text-sm text-blue-800 bg-blue-100 p-3 rounded">
                        {rca_report.analysis_summary}
                      </pre>
                    </div>
                  </div>
                  <div className="text-xs text-gray-500">
                    Analysis created: {new Date(rca_report.created_at).toLocaleString()}
                  </div>
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <Clock className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                  <p>No RCA analysis available for this error</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorDetail; 