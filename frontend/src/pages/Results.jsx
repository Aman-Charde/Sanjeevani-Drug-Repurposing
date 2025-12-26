import { useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import api from "../services/api";

export default function Results() {
    const location = useLocation();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [progress, setProgress] = useState(0);
    const [activeSection, setActiveSection] = useState(null);

    const query = location.state?.query || "";

    const navItems = [
        {
            label: "About",
            bgColor: "#0D0716",
            textColor: "#ffffff",
            links: [
                { label: "What we do", ariaLabel: "About project", to: "/about1" },
                { label: "Problem we solve", ariaLabel: "About project", to: "/about1" },
                { label: "Why Drug Repurposing", ariaLabel: "About project", to: "/about1" }
            ]
        },
        {
            label: "Technology",
            bgColor: "#170D27",
            textColor: "#ffffff",
            links: [
                { label: "AI Models", ariaLabel: "AI Models", to: "/technology" },
                { label: "Tech Stack", ariaLabel: "Tech Stack", to: "/technology" }
            ]
        },
        {
            label: "Contact",
            bgColor: "#0f0029ff",
            textColor: "#ffffff",
            links: [
                { label: "Email", ariaLabel: "Email", to: "/about" },
                { label: "LinkedIn", ariaLabel: "LinkedIn", to: "/about" },
                { label: "Github", ariaLabel: "Github", to: "/about" }
            ]
        }
    ];

    useEffect(() => {
        if (!query) {
            navigate("/dashboard");
            return;
        }

        const fetchResults = async () => {
            setLoading(true);
            setProgress(0);
            setError(null);

            const progressInterval = setInterval(() => {
                setProgress(prev => {
                    if (prev >= 90) return prev;
                    return prev + Math.random() * 15;
                });
            }, 500);

            try {
                const response = await api.post("/rag/query", {
                    query: query,
                    output_format: "text",
                    include_charts: true,
                    include_tables: true,
                    generate_report: false
                });

                clearInterval(progressInterval);
                setProgress(100);

                if (response.data.success) {
                    setResult(response.data);
                } else {
                    setError(response.data.error || "Failed to get results");
                }
            } catch (err) {
                clearInterval(progressInterval);
                console.error("Error fetching results:", err);
                setError(
                    err.response?.data?.error ||
                    err.response?.data?.message ||
                    "Failed to connect to the AI service. Please ensure the RAG agents server is running."
                );
            } finally {
                setLoading(false);
            }
        };

        fetchResults();
    }, [query, navigate]);

    // Section icons mapping
    const sectionIcons = {
        'executive summary': '📋',
        'summary': '📋',
        'research': '🔬',
        'analysis': '📊',
        'market': '💹',
        'iqvia': '📈',
        'clinical': '🏥',
        'trials': '🧪',
        'patent': '📜',
        'intellectual': '⚖️',
        'reference': '📚',
        'source': '🔗',
        'recommendation': '💡',
        'conclusion': '✅',
        'overview': '🎯',
        'mechanism': '⚙️',
        'drug': '💊',
        'safety': '🛡️',
        'efficacy': '📉',
        'default': '📌'
    };

    const getSectionIcon = (title) => {
        const lowerTitle = title.toLowerCase();
        for (const [key, icon] of Object.entries(sectionIcons)) {
            if (lowerTitle.includes(key)) return icon;
        }
        return sectionIcons.default;
    };

    // Format text with markdown-style bold, italic, and inline code
    const formatText = (text) => {
        if (!text) return text;

        // Clean up the text first - remove excessive asterisks that aren't valid markdown
        let cleanedText = text
            .replace(/\*{3,}/g, '') // Remove 3+ asterisks
            .replace(/\*\*\s*\*\*/g, '') // Remove empty bold markers
            .trim();

        // Split text into parts to handle markdown formatting
        const parts = [];
        let remaining = cleanedText;
        let key = 0;

        // Regex patterns for markdown
        const patterns = [
            { regex: /\*\*([^*]+)\*\*/g, type: 'bold' },
            { regex: /\*([^*]+)\*/g, type: 'italic' },
            { regex: /`([^`]+)`/g, type: 'code' },
        ];

        // Process bold first
        const boldRegex = /\*\*([^*]+)\*\*/;
        const italicRegex = /(?<!\*)\*([^*]+)\*(?!\*)/;
        const codeRegex = /`([^`]+)`/;

        while (remaining.length > 0) {
            const boldMatch = remaining.match(boldRegex);
            const italicMatch = remaining.match(italicRegex);
            const codeMatch = remaining.match(codeRegex);

            // Find the earliest match
            let earliest = null;
            let earliestIndex = remaining.length;
            let matchType = null;

            if (boldMatch && boldMatch.index < earliestIndex) {
                earliest = boldMatch;
                earliestIndex = boldMatch.index;
                matchType = 'bold';
            }
            if (italicMatch && italicMatch.index < earliestIndex) {
                earliest = italicMatch;
                earliestIndex = italicMatch.index;
                matchType = 'italic';
            }
            if (codeMatch && codeMatch.index < earliestIndex) {
                earliest = codeMatch;
                earliestIndex = codeMatch.index;
                matchType = 'code';
            }

            if (earliest) {
                // Add text before the match
                if (earliestIndex > 0) {
                    parts.push(remaining.substring(0, earliestIndex));
                }

                // Add the formatted element
                const content = earliest[1];
                if (matchType === 'bold') {
                    parts.push(
                        <strong key={key++} className="font-semibold text-white">
                            {content}
                        </strong>
                    );
                } else if (matchType === 'italic') {
                    parts.push(
                        <em key={key++} className="italic text-purple-200">
                            {content}
                        </em>
                    );
                } else if (matchType === 'code') {
                    parts.push(
                        <code key={key++} className="px-1.5 py-0.5 rounded bg-white/10 text-cyan-300 text-sm font-mono">
                            {content}
                        </code>
                    );
                }

                remaining = remaining.substring(earliestIndex + earliest[0].length);
            } else {
                // No more matches, add the rest
                parts.push(remaining);
                break;
            }
        }

        return parts.length > 0 ? parts : cleanedText;
    };

    // Clean a text string by removing markdown symbols while keeping content
    const cleanText = (text) => {
        if (!text) return text;
        return text
            .replace(/\*\*([^*]+)\*\*/g, '$1')  // Remove bold markers
            .replace(/\*([^*]+)\*/g, '$1')      // Remove italic markers
            .replace(/`([^`]+)`/g, '$1')        // Remove code markers
            .replace(/\*+/g, '')                // Remove any remaining asterisks
            .trim();
    };

    // Parse markdown-style tables
    const parseTable = (tableText) => {
        const lines = tableText.trim().split('\n').filter(line => line.trim());
        if (lines.length < 2) return null;

        const parseRow = (row) => {
            return row.split('|')
                .map(cell => cell.trim())
                .filter(cell => cell && !cell.match(/^[-:]+$/));
        };

        const headers = parseRow(lines[0]);
        if (headers.length === 0) return null;

        // Skip separator line if present
        const dataStartIndex = lines[1]?.includes('-') ? 2 : 1;
        const rows = lines.slice(dataStartIndex).map(parseRow).filter(row => row.length > 0);

        return { headers, rows };
    };

    // Render a beautiful table
    const renderTable = (tableData, index) => {
        if (!tableData || !tableData.headers || tableData.headers.length === 0) return null;

        return (
            <div key={index} className="my-6 overflow-hidden rounded-xl border border-white/10 bg-gradient-to-b from-white/5 to-transparent">
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="bg-gradient-to-r from-purple-900/50 to-pink-900/50">
                                {tableData.headers.map((header, i) => (
                                    <th
                                        key={i}
                                        className="px-4 py-3 text-left text-sm font-semibold text-purple-200 border-b border-white/10 whitespace-nowrap"
                                    >
                                        {cleanText(header)}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {tableData.rows.map((row, rowIndex) => (
                                <tr
                                    key={rowIndex}
                                    className={`transition-colors hover:bg-white/5 ${rowIndex % 2 === 0 ? 'bg-white/[0.02]' : ''}`}
                                >
                                    {row.map((cell, cellIndex) => (
                                        <td
                                            key={cellIndex}
                                            className="px-4 py-3 text-sm text-gray-300 border-b border-white/5"
                                        >
                                            {formatText(cell)}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    };

    // Parse and structure the response
    const parseResponse = (text) => {
        if (!text) return [];

        const sections = [];
        let currentSection = null;
        let currentContent = [];

        const lines = text.split('\n');

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const trimmedLine = line.trim();

            // Check for main headers (# or ##)
            if (trimmedLine.startsWith('# ') || trimmedLine.startsWith('## ')) {
                // Save previous section
                if (currentSection) {
                    sections.push({
                        ...currentSection,
                        content: currentContent.join('\n')
                    });
                }

                const level = trimmedLine.startsWith('## ') ? 2 : 1;
                const title = cleanText(trimmedLine.replace(/^#{1,2}\s*/, ''));

                currentSection = {
                    level,
                    title,
                    icon: getSectionIcon(title)
                };
                currentContent = [];
            } else {
                currentContent.push(line);
            }
        }

        // Don't forget the last section
        if (currentSection) {
            sections.push({
                ...currentSection,
                content: currentContent.join('\n')
            });
        }

        // If no sections found, create a default one
        if (sections.length === 0) {
            sections.push({
                level: 1,
                title: 'Analysis Results',
                icon: '📊',
                content: text
            });
        }

        return sections;
    };

    // Render section content
    const renderContent = (content) => {
        if (!content || !content.trim()) return null;

        const elements = [];
        const lines = content.split('\n');
        let currentTable = [];
        let inTable = false;
        let paragraphBuffer = [];

        const flushParagraph = () => {
            if (paragraphBuffer.length > 0) {
                const text = paragraphBuffer.join(' ').trim();
                if (text) {
                    elements.push(
                        <p key={`p-${elements.length}`} className="text-gray-300 leading-relaxed mb-4">
                            {formatText(text)}
                        </p>
                    );
                }
                paragraphBuffer = [];
            }
        };

        const flushTable = () => {
            if (currentTable.length > 0) {
                const tableData = parseTable(currentTable.join('\n'));
                if (tableData) {
                    elements.push(renderTable(tableData, `table-${elements.length}`));
                }
                currentTable = [];
                inTable = false;
            }
        };

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const trimmedLine = line.trim();

            // Skip empty lines
            if (!trimmedLine) {
                if (inTable) flushTable();
                flushParagraph();
                continue;
            }

            // Check for sub-headers (### or ####)
            if (trimmedLine.startsWith('### ') || trimmedLine.startsWith('#### ')) {
                if (inTable) flushTable();
                flushParagraph();
                const headerText = cleanText(trimmedLine.replace(/^#{3,4}\s*/, ''));
                elements.push(
                    <h4 key={`h4-${elements.length}`} className="text-lg font-semibold text-purple-300 mt-6 mb-3 flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-purple-400" />
                        {headerText}
                    </h4>
                );
                continue;
            }

            // Check for table row (contains |)
            if (trimmedLine.includes('|')) {
                flushParagraph();
                inTable = true;
                currentTable.push(trimmedLine);
                continue;
            }

            // If we were in a table, flush it
            if (inTable) {
                flushTable();
            }

            // Check for bullet points
            if (trimmedLine.startsWith('- ') || trimmedLine.startsWith('• ') || trimmedLine.startsWith('* ')) {
                flushParagraph();
                const bulletText = trimmedLine.replace(/^[-•*]\s*/, '');

                // Check if next lines are also bullets for grouping
                const bulletItems = [bulletText];
                while (i + 1 < lines.length) {
                    const nextLine = lines[i + 1].trim();
                    if (nextLine.startsWith('- ') || nextLine.startsWith('• ') || nextLine.startsWith('* ')) {
                        bulletItems.push(nextLine.replace(/^[-•*]\s*/, ''));
                        i++;
                    } else {
                        break;
                    }
                }

                elements.push(
                    <ul key={`ul-${elements.length}`} className="space-y-2 my-4 ml-4">
                        {bulletItems.map((item, idx) => (
                            <li key={idx} className="flex items-start gap-3 text-gray-300">
                                <span className="mt-2 w-1.5 h-1.5 rounded-full bg-gradient-to-r from-purple-400 to-pink-400 flex-shrink-0" />
                                <span className="leading-relaxed">{formatText(item)}</span>
                            </li>
                        ))}
                    </ul>
                );
                continue;
            }

            // Check for numbered lists
            if (/^\d+[.)]\s/.test(trimmedLine)) {
                flushParagraph();
                const itemText = trimmedLine.replace(/^\d+[.)]\s*/, '');

                const numberItems = [itemText];
                while (i + 1 < lines.length) {
                    const nextLine = lines[i + 1].trim();
                    if (/^\d+[.)]\s/.test(nextLine)) {
                        numberItems.push(nextLine.replace(/^\d+[.)]\s*/, ''));
                        i++;
                    } else {
                        break;
                    }
                }

                elements.push(
                    <ol key={`ol-${elements.length}`} className="space-y-2 my-4 ml-4">
                        {numberItems.map((item, idx) => (
                            <li key={idx} className="flex items-start gap-3 text-gray-300">
                                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center text-xs font-semibold text-white">
                                    {idx + 1}
                                </span>
                                <span className="leading-relaxed pt-0.5">{formatText(item)}</span>
                            </li>
                        ))}
                    </ol>
                );
                continue;
            }

            // Check for key-value pairs (Key: Value)
            const kvMatch = trimmedLine.match(/^([A-Za-z\s]+):\s*(.+)$/);
            if (kvMatch && kvMatch[1].length < 30) {
                flushParagraph();
                elements.push(
                    <div key={`kv-${elements.length}`} className="flex items-start gap-2 my-2 py-2 px-3 rounded-lg bg-white/5 border-l-2 border-purple-500">
                        <span className="font-medium text-purple-300 min-w-[120px]">{cleanText(kvMatch[1])}:</span>
                        <span className="text-gray-300">{formatText(kvMatch[2])}</span>
                    </div>
                );
                continue;
            }

            // Regular text - add to paragraph buffer
            paragraphBuffer.push(trimmedLine);
        }

        // Flush remaining content
        if (inTable) flushTable();
        flushParagraph();

        return elements;
    };

    const sections = result ? parseResponse(result.response) : [];

    return (
        <div className="relative min-h-screen bg-[#050816] text-white">
            {/* Background gradient effects */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl" />
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl" />
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-pink-500/5 rounded-full blur-3xl" />
            </div>

            {/* Navbar */}
            <div className="relative z-50">
                <Navbar items={navItems} isLoggedIn={true} />
            </div>

            {/* Main Content */}
            <section className="relative z-10 px-4 md:px-8 pt-28 pb-20 min-h-screen">
                <div className="max-w-6xl mx-auto">

                    {/* Back Button */}
                    <button
                        onClick={() => navigate("/dashboard")}
                        className="group flex items-center gap-2 text-gray-400 hover:text-white transition-colors duration-300 mb-8"
                    >
                        <svg className="w-5 h-5 group-hover:-translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                        <span>Back to Dashboard</span>
                    </button>

                    {/* Query Display */}
                    <div className="mb-8">
                        <p className="text-sm text-purple-400 mb-2 font-medium">Your Research Query</p>
                        <div className="relative group">
                            <div className="absolute -inset-[1px] bg-gradient-to-r from-purple-500 via-pink-500 to-cyan-500 rounded-xl opacity-40 blur-sm group-hover:opacity-60 transition-opacity" />
                            <div className="relative bg-white/5 backdrop-blur-xl rounded-xl p-5 border border-white/10">
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center flex-shrink-0">
                                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                        </svg>
                                    </div>
                                    <p className="text-lg text-white font-medium">{query}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Loading State */}
                    {loading && (
                        <div className="flex flex-col items-center justify-center py-20">
                            <div className="relative">
                                <div className="w-24 h-24 rounded-full border-4 border-purple-500/30 border-t-purple-500 animate-spin" />
                                <div className="absolute inset-0 flex items-center justify-center">
                                    <span className="text-2xl">🧬</span>
                                </div>
                            </div>

                            <h3 className="mt-8 text-xl font-semibold text-white">Analyzing Your Query...</h3>
                            <p className="mt-2 text-gray-400 text-center max-w-md">
                                Our multi-agent AI system is researching drug repurposing insights
                            </p>

                            <div className="w-full max-w-md mt-8">
                                <div className="flex justify-between text-sm text-gray-400 mb-2">
                                    <span>Progress</span>
                                    <span>{Math.round(progress)}%</span>
                                </div>
                                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-gradient-to-r from-purple-500 via-pink-500 to-cyan-500 rounded-full transition-all duration-300"
                                        style={{ width: `${progress}%` }}
                                    />
                                </div>
                            </div>

                            <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
                                {["Market Analysis", "Patent Search", "Clinical Trials", "Data Synthesis"].map((agent, i) => (
                                    <div
                                        key={agent}
                                        className={`px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-center transition-all duration-500 ${progress > (i + 1) * 20 ? "border-green-500/50 bg-green-500/5" : ""}`}
                                    >
                                        <div className={`w-2 h-2 rounded-full mx-auto mb-2 ${progress > (i + 1) * 20 ? "bg-green-400" : "bg-purple-400 animate-pulse"}`} />
                                        <p className="text-xs text-gray-400">{agent}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Error State */}
                    {error && !loading && (
                        <div className="flex flex-col items-center justify-center py-20">
                            <div className="w-20 h-20 rounded-full bg-red-500/10 flex items-center justify-center mb-6">
                                <svg className="w-10 h-10 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <h3 className="text-xl font-semibold text-white mb-2">Something went wrong</h3>
                            <p className="text-gray-400 text-center max-w-md mb-6">{error}</p>
                            <div className="flex gap-4">
                                <button
                                    onClick={() => window.location.reload()}
                                    className="px-6 py-3 rounded-lg bg-purple-600 hover:bg-purple-700 text-white font-medium transition-colors"
                                >
                                    Try Again
                                </button>
                                <button
                                    onClick={() => navigate("/dashboard")}
                                    className="px-6 py-3 rounded-lg bg-white/10 hover:bg-white/20 text-white font-medium transition-colors"
                                >
                                    New Search
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Results Display */}
                    {result && !loading && (
                        <div className="space-y-6">
                            {/* Success Header */}
                            <div className="flex items-center justify-between flex-wrap gap-4 p-5 rounded-xl bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/30">
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-full bg-green-500/20 flex items-center justify-center">
                                        <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                        </svg>
                                    </div>
                                    <div>
                                        <p className="text-green-400 font-semibold text-lg">Analysis Complete</p>
                                        <p className="text-sm text-gray-400">
                                            Processed by {result.agent_count || "multiple"} AI agents in {result.execution_time_ms ? `${(result.execution_time_ms / 1000).toFixed(2)}s` : "a few seconds"}
                                        </p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-2 text-sm text-gray-400">
                                    <span className="px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 font-medium">
                                        {sections.length} Sections
                                    </span>
                                </div>
                            </div>

                            {/* Quick Navigation (Table of Contents) */}
                            {sections.length > 1 && (
                                <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                                    <p className="text-sm font-medium text-gray-400 mb-3">Jump to Section</p>
                                    <div className="flex flex-wrap gap-2">
                                        {sections.map((section, index) => (
                                            <button
                                                key={index}
                                                onClick={() => {
                                                    setActiveSection(index);
                                                    document.getElementById(`section-${index}`)?.scrollIntoView({ behavior: 'smooth' });
                                                }}
                                                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-300 flex items-center gap-2 ${activeSection === index
                                                    ? 'bg-purple-600 text-white'
                                                    : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
                                                    }`}
                                            >
                                                <span>{section.icon}</span>
                                                <span>{section.title}</span>
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Main Response - Structured Sections */}
                            <div className="space-y-6">
                                {sections.map((section, index) => (
                                    <div
                                        key={index}
                                        id={`section-${index}`}
                                        className="relative group scroll-mt-32"
                                    >
                                        {/* Section Card */}
                                        <div className="absolute -inset-[1px] bg-gradient-to-r from-purple-500/20 via-pink-500/20 to-cyan-500/20 rounded-2xl blur-sm opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                                        <div className="relative bg-[#0a0f1e]/90 backdrop-blur-xl rounded-2xl border border-white/10 overflow-hidden">

                                            {/* Section Header */}
                                            <div className="p-5 border-b border-white/10 bg-gradient-to-r from-purple-900/20 to-pink-900/20">
                                                <div className="flex items-center gap-4">
                                                    <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center text-xl">
                                                        {section.icon}
                                                    </div>
                                                    <div>
                                                        <h2 className="text-xl font-bold text-white">
                                                            {section.title}
                                                        </h2>
                                                        <p className="text-sm text-gray-400">Section {index + 1} of {sections.length}</p>
                                                    </div>
                                                </div>
                                            </div>

                                            {/* Section Content */}
                                            <div className="p-6">
                                                {renderContent(section.content)}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Action Buttons */}
                            <div className="flex flex-wrap gap-4 justify-center pt-8 pb-4">
                                <button
                                    onClick={() => navigate("/dashboard")}
                                    className="px-8 py-3.5 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/25 flex items-center gap-2"
                                >
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                    </svg>
                                    New Search
                                </button>
                                <button
                                    onClick={() => {
                                        navigator.clipboard.writeText(result.response || "");
                                        const btn = event.currentTarget;
                                        btn.textContent = "✓ Copied!";
                                        setTimeout(() => {
                                            btn.innerHTML = `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>Copy Results`;
                                        }, 2000);
                                    }}
                                    className="px-6 py-3.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-medium transition-colors flex items-center gap-2"
                                >
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                    </svg>
                                    Copy Results
                                </button>
                                <button
                                    onClick={() => window.print()}
                                    className="px-6 py-3.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-medium transition-colors flex items-center gap-2"
                                >
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                                    </svg>
                                    Print Report
                                </button>
                            </div>

                            {/* Scroll to Top */}
                            <div className="flex justify-center">
                                <button
                                    onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                                    className="text-gray-500 hover:text-white transition-colors text-sm flex items-center gap-2"
                                >
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
                                    </svg>
                                    Back to Top
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </section>

            <Footer />
        </div>
    );
}
