import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  Database, 
  Search, 
  RefreshCw, 
  AlertTriangle, 
  Clock, 
  Server, 
  Code, 
  Activity,
  ExternalLink
} from 'lucide-react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Dashboard = () => {
  const [errors, setErrors] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [expandedError, setExpandedError] = useState(null);
  const [activeView, setActiveView] = useState('overview');
  const [detailedErrorData, setDetailedErrorData] = useState({});
  const [highlightedError, setHighlightedError] = useState(null);

  // Check for highlight parameter on mount
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const highlight = urlParams.get('highlight');
    if (highlight) {
      setHighlightedError(highlight);
      // Auto-expand the highlighted error after data loads
      setTimeout(() => {
        const errorElement = document.getElementById(`error-${highlight}`);
        if (errorElement) {
          errorElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
          errorElement.classList.add('ring-2', 'ring-blue-500', 'ring-opacity-50');
        }
      }, 1000);
    }
  }, []);

  const fetchData = async () => {
    try {
      const [errorsResponse, statsResponse] = await Promise.all([
        fetch('/api/errors?env=&service=&hours=24'),
        fetch('/api/stats')
      ]);
      
      const errorsData = await errorsResponse.json();
      const statsData = await statsResponse.json();
      
      // Handle the correct API response structure
      setErrors(errorsData.errors || []);
      setStats(statsData);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const toggleErrorDetails = async (errorId) => {
    if (expandedError === errorId) {
      setExpandedError(null);
      setActiveView('overview');
      setDetailedErrorData({});
    } else {
      setExpandedError(errorId);
      setActiveView('overview');
      
      // Fetch detailed error data
      try {
        const response = await axios.get(`/api/errors/${errorId}`);
        setDetailedErrorData(response.data);
      } catch (error) {
        console.error('Error fetching error details:', error);
      }
    }
  };

  // Calculate time until next 5-minute boundary for sync
  const getTimeUntilNextSync = () => {
    const now = new Date();
    const minutes = now.getMinutes();
    const seconds = now.getSeconds();
    const nextBoundary = Math.ceil(minutes / 5) * 5;
    const waitMinutes = nextBoundary - minutes;
    const waitSeconds = (waitMinutes * 60) - seconds;
    return Math.max(0, waitSeconds * 1000);
  };

  useEffect(() => {
    fetchData();
    
    // Initial sync timing
    const initialTimeout = setTimeout(() => {
      fetchData();
      // Then sync every 5 minutes
      const interval = setInterval(fetchData, 5 * 60 * 1000);
      return () => clearInterval(interval);
    }, getTimeUntilNextSync());
    
    return () => clearTimeout(initialTimeout);
  }, []);

  // Chart colors
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

  const renderTracesView = (detailedData) => {
    const traces = detailedData.traces || [];
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-800">Traces</h3>
        {traces && traces.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-200 rounded-lg">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trace ID (Hex)</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trace ID (Base64)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {traces.map((trace, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-4 py-2 text-sm font-mono text-gray-900">{trace.trace_id_hex}</td>
                    <td className="px-4 py-2 text-sm font-mono text-gray-600">{trace.trace_id_b64}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <Database className="mx-auto h-12 w-12 text-gray-400" />
            <p className="mt-2">No traces found</p>
          </div>
        )}
      </div>
    );
  };

  const renderSpansView = (detailedData) => {
    const spans = detailedData.spans || [];
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-800">Spans</h3>
        {spans && spans.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-200 rounded-lg">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trace ID</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Span ID</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Operation</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Duration (ms)</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Start Time</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tags</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {spans.map((span, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-4 py-2 text-sm font-mono text-gray-900">{span.trace_id_hex}</td>
                    <td className="px-4 py-2 text-sm font-mono text-gray-900">{span.span_id}</td>
                    <td className="px-4 py-2 text-sm text-gray-600">{span.operation_name || 'N/A'}</td>
                    <td className="px-4 py-2 text-sm text-gray-600">{span.duration ? `${(span.duration * 1000).toFixed(2)}` : 'N/A'}</td>
                    <td className="px-4 py-2 text-sm text-gray-600">
                      {span.start_time ? new Date(span.start_time).toLocaleString() : 'N/A'}
                    </td>
                    <td className="px-4 py-2 text-sm text-gray-600">
                      {span.tags ? (
                        <div className="max-w-xs">
                          {Object.entries(span.tags).map(([key, value]) => (
                            <div key={key} className="text-xs">
                              <span className="font-medium">{key}:</span> {String(value)}
                            </div>
                          ))}
                        </div>
                      ) : (
                        'N/A'
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <Database className="mx-auto h-12 w-12 text-gray-400" />
            <p className="mt-2">No spans found</p>
          </div>
        )}
      </div>
    );
  };

  const renderLogsView = (detailedData) => {
    const logs = detailedData.logs || [];
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-800">Logs</h3>
        {logs && logs.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-200 rounded-lg">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trace ID</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Log Level</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Message</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {logs.map((log, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-4 py-2 text-sm font-mono text-gray-900">{log.trace_id_hex}</td>
                    <td className="px-4 py-2 text-sm text-gray-600">{log.log_data?.level || 'N/A'}</td>
                    <td className="px-4 py-2 text-sm text-gray-600">{log.log_data?.message || 'N/A'}</td>
                    <td className="px-4 py-2 text-sm text-gray-600">{log.log_data?.timestamp || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <FileText className="mx-auto h-12 w-12 text-gray-400" />
            <p className="mt-2">No logs found</p>
          </div>
        )}
      </div>
    );
  };

  const renderCorrelationView = (detailedData) => {
    const error = detailedData.error || {};
    const traces = detailedData.traces || [];
    const spans = detailedData.spans || [];
    const logs = detailedData.logs || [];
    
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-800">Correlation Data</h3>
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Error Metrics</h4>
              <div className="space-y-2 text-sm">
                <div><span className="font-medium">Environment:</span> {error.env}</div>
                <div><span className="font-medium">Service:</span> {error.service}</div>
                <div><span className="font-medium">Span Kind:</span> {error.span_kind}</div>
                <div><span className="font-medium">HTTP Code:</span> {error.http_code}</div>
                <div><span className="font-medium">Exception:</span> {error.exception}</div>
                <div><span className="font-medium">Root Name:</span> {error.root_name}</div>
                <div><span className="font-medium">Count:</span> {error.count}</div>
                <div><span className="font-medium">Window:</span> {error.window_start} - {error.window_end}</div>
              </div>
            </div>
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Trace & Log Summary</h4>
              <div className="space-y-2 text-sm">
                <div><span className="font-medium">Traces Found:</span> {traces.length}</div>
                <div><span className="font-medium">Spans Found:</span> {spans.length}</div>
                <div><span className="font-medium">Logs Found:</span> {logs.length}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderRCAView = (detailedData) => {
    const rcaReport = detailedData.rca_report;
    
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-800">RCA Analysis</h3>
        {rcaReport ? (
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap text-sm text-gray-800 bg-gray-50 p-4 rounded">
                {rcaReport.analysis_summary}
              </pre>
            </div>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <Search className="mx-auto h-12 w-12 text-gray-400" />
            <p className="mt-2">No RCA analysis available</p>
          </div>
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="mx-auto h-8 w-8 text-blue-600 animate-spin" />
          <p className="mt-2 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">RCA Platform Dashboard</h1>
          <p className="mt-2 text-gray-600">Real-time error monitoring and root cause analysis</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <AlertTriangle className="h-8 w-8 text-red-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Errors</p>
                <p className="text-2xl font-bold text-gray-900">{stats.last_24_hours?.total_errors || 0}</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Server className="h-8 w-8 text-blue-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Services</p>
                <p className="text-2xl font-bold text-gray-900">{stats.last_24_hours?.top_services?.length || 0}</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Database className="h-8 w-8 text-green-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Traces</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total_data?.traces || 0}</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <FileText className="h-8 w-8 text-purple-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Logs</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total_data?.logs || 0}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Analytics Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Environment Distribution */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Errors by Environment</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stats.last_24_hours?.environments || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="env" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Service Distribution */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Errors by Service</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={stats.last_24_hours?.top_services || []}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ service, percent }) => `${service} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {stats.last_24_hours?.top_services?.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Refresh Button */}
        <div className="mb-6 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-900">Error Cards</h2>
          <button
            onClick={fetchData}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </button>
        </div>

        {/* Error Cards */}
        <div className="space-y-4">
          {(errors || []).map((error) => (
            <div
              key={error.id}
              id={`error-${error.id}`}
              className={`bg-white rounded-lg shadow border-2 transition-all duration-200 ${
                highlightedError === error.id ? 'border-blue-500' : 'border-transparent'
              }`}
            >
              {/* Error Card Header */}
              <div className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-4">
                      <AlertTriangle className="h-6 w-6 text-red-500" />
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 truncate">
                          {error.service}
                        </h3>
                        <div className="mt-1 text-sm text-gray-600">
                          <span className="font-medium">Exception:</span> {error.exception}
                        </div>
                        <div className="mt-1 text-sm text-gray-600">
                          <span className="font-medium">Root Name:</span> {error.root_name || 'N/A'}
                        </div>
                      </div>
                    </div>
                    <div className="mt-3 flex items-center space-x-4 text-sm text-gray-600">
                      <span className="flex items-center">
                        <Server className="h-4 w-4 mr-1" />
                        {error.env}
                      </span>
                      <span className="flex items-center">
                        <Code className="h-4 w-4 mr-1" />
                        {error.http_code}
                      </span>
                      <span className="flex items-center">
                        <Activity className="h-4 w-4 mr-1" />
                        {error.span_kind}
                      </span>
                      <span className="flex items-center">
                        <Clock className="h-4 w-4 mr-1" />
                        {error.count} occurrences
                      </span>
                    </div>
                    <div className="mt-2 text-xs text-gray-500">
                      <span className="font-medium">Time Window:</span> {error.window_start} - {error.window_end}
                    </div>
                    <div className="mt-2 flex items-center space-x-2">
                      <a
                        href={`${window.location.origin}/dashboard?highlight=${error.id}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-xs text-blue-600 hover:text-blue-800"
                      >
                        <ExternalLink className="h-3 w-3 mr-1" />
                        Share Error Link
                      </a>
                    </div>
                  </div>
                  <button
                    onClick={() => toggleErrorDetails(error.id)}
                    className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    {expandedError === error.id ? 'Hide Details' : 'View Details'}
                  </button>
                </div>
              </div>

              {/* Expanded Details */}
              {expandedError === error.id && (
                <div className="border-t border-gray-200 p-6">
                  {/* View Buttons */}
                  <div className="flex space-x-2 mb-6">
                    <button
                      onClick={() => setActiveView('overview')}
                      className={`px-4 py-2 text-sm font-medium rounded-md ${
                        activeView === 'overview'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      Overview
                    </button>
                    <button
                      onClick={() => setActiveView('traces')}
                      className={`px-4 py-2 text-sm font-medium rounded-md ${
                        activeView === 'traces'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      Traces
                    </button>
                    <button
                      onClick={() => setActiveView('spans')}
                      className={`px-4 py-2 text-sm font-medium rounded-md ${
                        activeView === 'spans'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      Spans
                    </button>
                    <button
                      onClick={() => setActiveView('logs')}
                      className={`px-4 py-2 text-sm font-medium rounded-md ${
                        activeView === 'logs'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      Logs
                    </button>
                    <button
                      onClick={() => setActiveView('correlation')}
                      className={`px-4 py-2 text-sm font-medium rounded-md ${
                        activeView === 'correlation'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      Correlation
                    </button>
                    <button
                      onClick={() => setActiveView('rca')}
                      className={`px-4 py-2 text-sm font-medium rounded-md ${
                        activeView === 'rca'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      RCA Analysis
                    </button>
                  </div>

                  {/* View Content */}
                  <div className="mt-4">
                    {activeView === 'overview' && (
                      <div className="space-y-4">
                        <h3 className="text-lg font-semibold text-gray-800">Error Overview</h3>
                        <div className="bg-gray-50 rounded-lg p-4">
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                              <h4 className="font-medium text-gray-700 mb-2">Error Details</h4>
                              <div className="space-y-2 text-sm">
                                <div><span className="font-medium">Environment:</span> {error.env}</div>
                                <div><span className="font-medium">Service:</span> {error.service}</div>
                                <div><span className="font-medium">Exception:</span> {error.exception}</div>
                                <div><span className="font-medium">Count:</span> {error.count}</div>
                              </div>
                            </div>
                            <div>
                              <h4 className="font-medium text-gray-700 mb-2">Time Window</h4>
                              <div className="space-y-2 text-sm">
                                <div><span className="font-medium">Start:</span> {error.window_start}</div>
                                <div><span className="font-medium">End:</span> {error.window_end}</div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                    {activeView === 'traces' && renderTracesView(detailedErrorData)}
                    {activeView === 'spans' && renderSpansView(detailedErrorData)}
                    {activeView === 'logs' && renderLogsView(detailedErrorData)}
                    {activeView === 'correlation' && renderCorrelationView(detailedErrorData)}
                    {activeView === 'rca' && renderRCAView(detailedErrorData)}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {(!errors || errors.length === 0) && (
          <div className="text-center py-12">
            <AlertTriangle className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No errors found</h3>
            <p className="mt-1 text-sm text-gray-500">No error cards have been detected in the last 24 hours.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard; 