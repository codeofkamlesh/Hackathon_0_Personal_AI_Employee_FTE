#!/usr/bin/env node
/**
 * Email MCP Server
 * Provides email sending capabilities for the Personal AI Employee
 * Part of Silver Tier implementation
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import nodemailer from 'nodemailer';

/**
 * Email MCP Server
 * Provides tools for sending emails with approval workflow
 */
class EmailMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'email-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    // Mock transporter for demo (replace with real SMTP in production)
    this.transporter = this.createMockTransporter();

    this.setupToolHandlers();

    // Error handling
    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  /**
   * Create mock email transporter for demonstration
   * In production, replace with real SMTP configuration:
   *
   * nodemailer.createTransport({
   *   host: 'smtp.gmail.com',
   *   port: 587,
   *   secure: false,
   *   auth: {
   *     user: process.env.EMAIL_USER,
   *     pass: process.env.EMAIL_PASSWORD
   *   }
   * });
   */
  createMockTransporter() {
    return {
      sendMail: async (mailOptions) => {
        // Mock implementation - logs instead of sending
        console.log('[MOCK EMAIL] Would send email:');
        console.log('  To:', mailOptions.to);
        console.log('  Subject:', mailOptions.subject);
        console.log('  Body:', mailOptions.text?.substring(0, 100) + '...');

        return {
          messageId: `mock-${Date.now()}@example.com`,
          accepted: [mailOptions.to],
          response: '250 Message accepted (MOCK)'
        };
      }
    };
  }

  /**
   * Setup MCP tool handlers
   */
  setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'send_email',
          description: 'Send an email to a recipient. Requires prior approval for sensitive actions.',
          inputSchema: {
            type: 'object',
            properties: {
              to: {
                type: 'string',
                description: 'Recipient email address',
              },
              subject: {
                type: 'string',
                description: 'Email subject line',
              },
              body: {
                type: 'string',
                description: 'Email body content (plain text)',
              },
              cc: {
                type: 'string',
                description: 'CC recipients (comma-separated)',
              },
              attachments: {
                type: 'array',
                items: { type: 'string' },
                description: 'Array of file paths to attach',
              },
            },
            required: ['to', 'subject', 'body'],
          },
        },
        {
          name: 'draft_email',
          description: 'Draft an email without sending (for approval workflow)',
          inputSchema: {
            type: 'object',
            properties: {
              to: {
                type: 'string',
                description: 'Recipient email address',
              },
              subject: {
                type: 'string',
                description: 'Email subject line',
              },
              body: {
                type: 'string',
                description: 'Email body content',
              },
            },
            required: ['to', 'subject', 'body'],
          },
        },
      ],
    }));

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        if (name === 'send_email') {
          return await this.handleSendEmail(args);
        } else if (name === 'draft_email') {
          return await this.handleDraftEmail(args);
        } else {
          throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  /**
   * Handle send_email tool call
   */
  async handleSendEmail(args) {
    const { to, subject, body, cc, attachments } = args;

    // Validate inputs
    if (!to || !subject || !body) {
      throw new Error('Missing required fields: to, subject, body');
    }

    // Prepare mail options
    const mailOptions = {
      from: process.env.EMAIL_FROM || 'ai-employee@example.com',
      to,
      subject,
      text: body,
      cc: cc || undefined,
      attachments: attachments?.map(path => ({ path })) || undefined,
    };

    // Send email
    const info = await this.transporter.sendMail(mailOptions);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            messageId: info.messageId,
            to,
            subject,
            timestamp: new Date().toISOString(),
          }, null, 2),
        },
      ],
    };
  }

  /**
   * Handle draft_email tool call
   */
  async handleDraftEmail(args) {
    const { to, subject, body } = args;

    // Validate inputs
    if (!to || !subject || !body) {
      throw new Error('Missing required fields: to, subject, body');
    }

    // Return draft (doesn't actually send)
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            action: 'draft_created',
            draft: {
              to,
              subject,
              body,
              created: new Date().toISOString(),
            },
            message: 'Email draft created. Move to approval workflow before sending.',
          }, null, 2),
        },
      ],
    };
  }

  /**
   * Start the MCP server
   */
  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Email MCP Server running on stdio');
  }
}

// Start server
const server = new EmailMCPServer();
server.run().catch(console.error);
