# How to Use the Agent Chat Feature

## Quick Start

### 1. Start the Dashboard
```bash
# Make sure your OpenAI API key is set
export OPENAI_API_KEY='your-key-here'

# Launch the dashboard
python3 examples/launch_dashboard.py
```

### 2. Open in Browser
Navigate to: **http://127.0.0.1:5000**

### 3. Select an Agent
Click on any agent card to open the agent detail modal.

**Recommended for first test**: Click on **Neil** (Staff Auditor) - confirmed working with GPT-4 Turbo

### 4. Open Chat Tab
Click the **"Chat"** tab in the modal (after Memory tab)

### 5. Start Chatting!
- Type your message in the input box
- Press **Enter** or click **Send**
- Wait for the agent to respond (you'll see a loading animation)
- Continue the conversation!

## Example Conversations

### With Esther (Senior Auditor)
```
You: "Esther, welcome to the audit team. Can you explain your role?"

Esther: "Thank you! As a Senior Auditor, I'm responsible for conducting 
risk assessments, performing control testing, collecting evidence, and 
documenting findings. I have access to AWS IAM tools and can query user 
accounts, roles, and policies. I work collaboratively with the team to 
ensure thorough audit execution."
```

### With Neil (Staff Auditor)
```
You: "Neil, what controls are you familiar with?"

Neil: "I specialize in encryption and network security controls. I can 
help with testing encryption at rest, encryption in transit, network 
segmentation, and security group configurations. I follow the procedures 
in my knowledge base and escalate complex issues to senior auditors."
```

### With Maurice (Audit Manager)
```
You: "Maurice, what's your role in the audit?"

Maurice: "I'm the Audit Manager overseeing the entire audit engagement. 
My responsibilities include leading the team, reviewing workpapers for 
quality assurance, resolving issues, coordinating team activities, and 
managing client relationships. I ensure the audit stays on schedule and 
meets quality standards."
```

### With Chuck (IT Manager)
```
You: "Chuck, how can you help with the audit?"

Chuck: "I'm the IT Manager at CloudRetail and serve as the primary point 
of contact for the audit team. I can provide evidence, answer questions 
about our AWS environment, coordinate with technical SMEs, and help 
facilitate the audit process. I'm here to support the auditors and ensure 
they have what they need."
```

## Features

### Real-time Responses
- Agents respond immediately using their full LLM capabilities
- Responses include their complete knowledge base and tools

### Message History
- All messages are displayed in chronological order
- User messages appear on the right (blue)
- Agent messages appear on the left (white)

### Loading Indicator
- Bouncing dots animation while waiting for response
- Input is disabled during processing

### Keyboard Shortcuts
- **Enter**: Send message
- **Shift+Enter**: New line (not implemented yet)

### Cost Tracking
- Each response shows tokens used and cost
- Helps monitor LLM usage

## Tips

### Best Practices
1. **Be specific**: Ask clear, focused questions
2. **Use context**: Agents remember the conversation history
3. **Test incrementally**: Start with simple questions, then get more complex
4. **Check capabilities**: Ask agents what they can do

### What to Ask
- "What is your role?"
- "What tools do you have access to?"
- "Can you explain [specific control]?"
- "How would you approach [specific task]?"
- "What knowledge do you have about [topic]?"

### Troubleshooting

#### Agent doesn't respond
- Check that OPENAI_API_KEY is set
- Verify the dashboard is running
- Check browser console for errors
- Try refreshing the page

#### Response is slow
- LLM calls can take 5-30 seconds
- Wait for the loading animation to complete
- Don't send multiple messages while waiting

#### Error messages
- "Agent not found": Refresh the page and try again
- "Message cannot be empty": Type a message before sending
- "Error: [details]": Check the dashboard terminal for more info

## Testing the Feature

### Automated Test
```bash
python3 test_chat_feature.py
```

This will:
- Verify the dashboard is running
- Send a test message to Neil
- Display the response and stats

### Manual Test Checklist
- [ ] Dashboard loads successfully
- [ ] Can click on agent card
- [ ] Chat tab appears
- [ ] Can type message
- [ ] Can send message (Enter or button)
- [ ] Loading animation appears
- [ ] Agent responds with intelligent answer
- [ ] Can send follow-up messages
- [ ] Conversation history is maintained

## Advanced Usage

### Multi-turn Conversations
The chat maintains conversation history, so you can have multi-turn conversations:

```
You: "What controls should we test first?"
Agent: "We should start with high-risk controls like IAM and access management..."

You: "Can you list the specific IAM controls?"
Agent: "Sure, the key IAM controls include: 1. User access reviews..."

You: "How would you test control #1?"
Agent: "To test user access reviews, I would..."
```

### Task Assignment
You can use chat to assign tasks to agents:

```
You: "Maurice, please assign Neil to test encryption controls"
Maurice: "I'll create a task for Neil to test encryption controls..."
```

### Evidence Requests
Ask Chuck for evidence:

```
You: "Chuck, can you provide the IAM user list?"
Chuck: "I'll gather the IAM user list for you. Let me query our AWS environment..."
```

## What's Next?

Future enhancements could include:
- Export chat history
- Clear chat button
- Message timestamps
- Typing indicators
- File attachments
- Code syntax highlighting
- Markdown rendering
- Chat session persistence across page reloads

## Need Help?

If you encounter issues:
1. Check the dashboard terminal for error messages
2. Check browser console (F12) for JavaScript errors
3. Verify your OpenAI API key is valid
4. Try restarting the dashboard
5. Test with Neil first (confirmed working)

Enjoy chatting with your audit agents! 🤖💬
