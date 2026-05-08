// Universe IDE VSCode Extension
// The universe's best AI agentic IDE

const vscode = require('vscode');
const { workspace, commands, window, languages } = vscode;

// ============================================================================
// CONFIGURATION
// ============================================================================

const CONFIG = {
    provider: 'anthropic',
    model: 'claude-sonnet-4-20250505',
    maxAgents: 100,
};

// ============================================================================
// UTILITIES
// ============================================================================

function getConfig() {
    return workspace.getConfiguration('universe.ide');
}

function showProgress(message) {
    return window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Universe IDE',
    }, (progress) => {
        progress.report({ message });
        return Promise.resolve();
    });
}

function showMessage(message, type = 'info') {
    switch (type) {
        case 'error':
            window.showErrorMessage(message);
            break;
        case 'warning':
            window.showWarningMessage(message);
            break;
        default:
            window.showInformationMessage(message);
    }
}

// ============================================================================
// CORE COMMANDS
// ============================================================================

async function startUniverseIDE() {
    try {
        await showProgress('Initializing Universe IDE...');
        
        // Import from universe_ide
        const universe = require('./universe_ide');
        
        // Create universe with agents
        const config = getConfig();
        const numAgents = config.get('maxAgents', 100);
        
        const cosmos = universe.cosmos(numAgents);
        
        showMessage(`🚀 Universe IDE started with ${cosmos.num_agents} agents!`, 'info');
        
        // Show sidebar
        vscode.commands.executeCommand('universe.ide.sidebar');
        
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

async function analyzeCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        showMessage('No active editor', 'warning');
        return;
    }
    
    const selection = editor.selection;
    const code = editor.document.getText(selection);
    
    if (!code.trim()) {
        showMessage('No code selected', 'warning');
        return;
    }
    
    try {
        await showProgress('Analyzing code...');
        
        // Use AI assistant
        const ai = require('./universe_ai_assist');
        const assistant = ai.get_ai_assistant();
        
        const result = assistant.analyze(code);
        
        // Show results
        const doc = await vscode.workspace.openTextDocument({
            content: `Analysis Results\n${'='.repeat(50)}\n\n${result.content}\n`,
            language: 'markdown',
        });
        
        await vscode.window.showTextDocument(doc);
        
        showMessage('Analysis complete!', 'info');
        
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

async function fixIssues() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        showMessage('No active editor', 'warning');
        return;
    }
    
    const document = editor.document;
    const code = document.getText();
    
    try {
        await showProgress('Fixing issues...');
        
        // Use AI fixer
        const ai = require('./universe_ai_assist');
        const assistant = ai.get_ai_assistant();
        
        const result = assistant.fix(code);
        
        // Apply fixes
        const edit = new vscode.EditBuilder();
        const fullRange = new vscode.Range(
            document.positionAt(0),
            document.positionAt(document.getText().length),
        );
        
        await editor.edit(builder => {
            builder.replace(fullRange, result.content);
        });
        
        showMessage('Issues fixed!', 'info');
        
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

async function explainCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        showMessage('No active editor', 'warning');
        return;
    }
    
    const selection = editor.selection;
    const code = editor.document.getText(selection);
    
    if (!code.trim()) {
        showMessage('No code selected', 'warning');
        return;
    }
    
    try {
        await showProgress('Explaining code...');
        
        // Use AI explainer
        const ai = require('./universe_ai_assist');
        const assistant = ai.get_ai_assistant();
        
        const result = assistant.explain(code);
        
        // Show in output channel
        const channel = window.createOutputChannel('Universe IDE');
        channel.appendLine('='.repeat(50));
        channel.appendLine('EXPLANATION');
        channel.appendLine('='.repeat(50));
        channel.appendLine('');
        channel.appendLine(result.content);
        channel.show();
        
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

async function generateCode() {
    const prompt = await window.showInputBox({
        prompt: 'What do you want to generate?',
        placeHolder: 'e.g., Create a function to sort a list',
    });
    
    if (!prompt) return;
    
    try {
        await showProgress('Generating code...');
        
        // Use code generator
        const codegen = require('./universe_codegen');
        const generator = codegen.get_code_generator();
        
        const result = generator.generate(prompt);
        
        // Insert at cursor
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            await editor.edit(builder => {
                builder.insert(editor.selection.active, result);
            });
        }
        
        showMessage('Code generated!', 'info');
        
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

// ============================================================================
// COMPLETION PROVIDER
// ============================================================================

class CompletionProvider {
    provideCompletionItems(document, position) {
        const line = document.lineAt(position);
        const text = line.text.substring(0, position.character);
        
        // Simple completion suggestions
        const suggestions = [
            { label: 'universe.ai', kind: vscode.CompletionItemKind.Snippet },
            { label: 'cosmos(100)', kind: vscode.CompletionItemKind.Function },
        ];
        
        return suggestions.map(s => {
            const item = new vscode.CompletionItem(s.label, s.kind);
            item.detail = 'Universe IDE';
            return item;
        });
    }
}

// ============================================================================
// HOVER PROVIDER
// ============================================================================

class HoverProvider {
    provideHover(document, position) {
        const range = document.getWordRangeAtPosition(position);
        const word = document.getText(range);
        
        if (word.startsWith('universe.')) {
            return new vscode.Hover('Universe IDE: ' + word);
        }
        
        return null;
    }
}

// ============================================================================
// ACTIVATION
// ============================================================================

function activate(context) {
    console.log('🚀 Universe IDE activating...');
    
    // Register commands
    const commandList = [
        { id: 'universe.ide.start', handler: startUniverseIDE },
        { id: 'universe.ide.analyze', handler: analyzeCode },
        { id: 'universe.ide.fix', handler: fixIssues },
        { id: 'universe.ide.explain', handler: explainCode },
        { id: 'universe.ide.generate', handler: generateCode },
    ];
    
    commandList.forEach(cmd => {
        const disposable = commands.registerCommand(cmd.id, cmd.handler);
        context.subscriptions.push(disposable);
    });
    
    // Register completion provider
    const completionProvider = new CompletionProvider();
    const completionDisposable = languages.registerCompletionItemProvider(
        { pattern: '**/*.{py,js,ts}' },
        completionProvider,
        '.'
    );
    context.subscriptions.push(completionDisposable);
    
    // Register hover provider
    const hoverProvider = new HoverProvider();
    const hoverDisposable = languages.registerHoverProvider(
        { pattern: '**/*.{py,js,ts}' },
        hoverProvider
    );
    context.subscriptions.push(hoverDisposable);
    
    console.log('✅ Universe IDE activated!');
}

function deactivate() {
    console.log('Universe IDE deactivated');
}

module.exports = { activate, deactivate };