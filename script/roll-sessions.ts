import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

const MEMORY_DIR = join(process.cwd(), 'memory');
const SESSIONS_FILE = join(MEMORY_DIR, 'sessions.json');

interface Session {
  start_time: string | null;
  end_time: string | null;
  todos: string[];
  completed: string[];
  errors: string[];
  active_project: string | null;
}

interface SessionsData {
  current_session: number;
  sessions: {
    [key: string]: Session;
  };
}

function rollSessions() {
  const data: SessionsData = JSON.parse(readFileSync(SESSIONS_FILE, 'utf-8'));
  const now = new Date().toISOString();

  // 1. Close the current session if it's open
  const currentKey = data.current_session.toString();
  const currentSession = data.sessions[currentKey];
  
  if (currentSession.start_time && !currentSession.end_time) {
    currentSession.end_time = now;
  }

  const pendingTodos = currentSession.todos.filter(t => !currentSession.completed.includes(t));

  // 2. Determine next session slot and roll if necessary
  let nextSessionKey: string;
  if (data.current_session < 3) {
    data.current_session++;
    nextSessionKey = data.current_session.toString();
  } else {
    // Rolling: 2 -> 1, 3 -> 2, new -> 3
    data.sessions['1'] = { ...data.sessions['2'] };
    data.sessions['2'] = { ...data.sessions['3'] };
    nextSessionKey = '3';
  }

  // 3. Initialize the new session
  data.sessions[nextSessionKey] = {
    start_time: now,
    end_time: null,
    todos: pendingTodos,
    completed: [],
    errors: [],
    active_project: currentSession.active_project
  };

  writeFileSync(SESSIONS_FILE, JSON.stringify(data, null, 2));
  console.log(`Rolled to session ${nextSessionKey}. Pending todos carried over: ${pendingTodos.length}`);
}

try {
  rollSessions();
} catch (error) {
  console.error('Failed to roll sessions:', error);
  process.exit(1);
}
