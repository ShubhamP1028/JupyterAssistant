(function() {
    if (window.__ds_assistant_injected__) return;
    window.__ds_assistant_injected__ = true;

    function isJupyterPage() {
        return (
            window.location.pathname.includes('/notebooks/') ||
            document.querySelector('.jp-Notebook') ||
            document.querySelector('#notebook-container')
        );
    }

    function buildSidebarHTML() {
        return `
        <div class="ds-header" align="center">
            <div class="ds-title">🤖 Assistant</div>
            <div class="ds-subtitle">AI for your notebook</div>
        </div>
        <div class="ds-content">
            <div class="ds-section-title">Ask your question</div>
            <textarea id="ds-input" class="ds-input" placeholder="e.g. Merge two DataFrames on 'id'"></textarea>
            <button id="ds-generate" class="ds-generate">Generate Code</button>
            <div id="ds-loading" class="ds-loading">Generating...</div>
            <div id="ds-output" class="ds-output"># Output will appear here</div>
            <div>
                <button id="ds-copy" class="ds-copy">Copy</button>
                <button id="ds-insert" class="ds-insert">Insert into Cell</button>
            </div>
        </div>`;
    }

    function injectUI() {
        if (!isJupyterPage()) return;

        if (document.getElementById('ds-sidebar')) return;

        const sidebar = document.createElement('div');
        sidebar.id = 'ds-sidebar';
        sidebar.className = 'ds-sidebar';
        sidebar.innerHTML = buildSidebarHTML();
        document.body.appendChild(sidebar);

        const toggle = document.createElement('button');
        toggle.id = 'ds-toggle';
        toggle.className = 'ds-toggle';
        toggle.title = 'Toggle Assistant';
        toggle.textContent = '≡';
        toggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            toggle.style.right = sidebar.classList.contains('collapsed') ? '20px' : '410px';
        });
        document.body.appendChild(toggle);

        wireEvents();
    }

    function getActiveEditorElement() {
        // JupyterLab
        const labActive = document.querySelector('.jp-Cell.jp-mod-active .jp-InputArea-editor');
        if (labActive) return labActive;
        // Classic Notebook
        const classicActive = document.querySelector('.cell.selected .input_area');
        return classicActive || null;
    }

    function getNotebookImports() {
        const editors = document.querySelectorAll('.jp-InputArea-editor, .input_area');
        const imports = new Set();
        editors.forEach(ed => {
            const text = ed.textContent || '';
            const matches = text.match(/^(?:from\s+[\w\.]+\s+import\s+[\w\*,\s]+|import\s+[\w\.,\s]+)$/gm);
            if (matches) matches.forEach(m => imports.add(m.trim()));
        });
        return Array.from(imports);
    }

    function contextualizePrompt(userQuery) {
        const active = getActiveEditorElement();
        const current = active ? (active.textContent || '').slice(0, 2000) : '';
        const imports = getNotebookImports();
        return `You are a helpful Data Science assistant for Jupyter Notebooks.\n\nCurrent context:\n- Current cell content: ${current || 'Empty cell'}\n- Available imports: ${imports.join(', ') || 'None detected'}\n\nProvide only the simplest, executable Python code. No comments. Wrap in triple backticks (python).\n\nTask: ${userQuery}`;
    }

    async function generate() {
        const input = document.getElementById('ds-input');
        const out = document.getElementById('ds-output');
        const loading = document.getElementById('ds-loading');
        const btn = document.getElementById('ds-generate');

        const q = (input.value || '').trim();
        if (!q) { alert('Please enter a question'); return; }

        loading.style.display = 'block';
        btn.disabled = true;
        out.textContent = '# Waiting for response...';

        try {
            const prompt = contextualizePrompt(q);
            const resp = await fetch('http://127.0.0.1:5050/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: prompt })
            });
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const data = await resp.json();
            out.textContent = data.answer || '# No content';
        } catch (e) {
            out.textContent = `# Error: ${e.message}`;
        } finally {
            loading.style.display = 'none';
            btn.disabled = false;
        }
    }

    function stripFences(text) {
        if (!text) return '';
        return text.replace(/^```python\n?|\n?```$/g, '').trim();
    }

    function insertIntoCell() {
        const out = document.getElementById('ds-output');
        const code = stripFences(out.textContent || '');
        if (!code) return;
        const editor = getActiveEditorElement();
        if (!editor) { alert('No active cell detected'); return; }
        // naive insert for both classic and lab DOMs
        editor.textContent = code;
        editor.dispatchEvent(new Event('input', { bubbles: true }));
    }

    function copyOutput() {
        const out = document.getElementById('ds-output');
        const code = stripFences(out.textContent || '');
        navigator.clipboard.writeText(code);
    }

    function wireEvents() {
        document.getElementById('ds-generate').addEventListener('click', generate);
        document.getElementById('ds-copy').addEventListener('click', copyOutput);
        document.getElementById('ds-insert').addEventListener('click', insertIntoCell);
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 'a') {
                const sidebar = document.getElementById('ds-sidebar');
                const toggle = document.getElementById('ds-toggle');
                sidebar.classList.toggle('collapsed');
                toggle.style.right = sidebar.classList.contains('collapsed') ? '20px' : '410px';
            }
        });
    }

    const observer = new MutationObserver(() => {
        if (!document.getElementById('ds-sidebar') && isJupyterPage()) {
            injectUI();
        }
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectUI);
    } else {
        injectUI();
    }
})();


