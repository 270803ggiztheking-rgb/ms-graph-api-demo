/**
 * MockGraphAPI Service
 * Simulates Microsoft Graph API responses for the static demo site.
 * This allows users to experience the application flow without actual backend integration.
 * Uses sessionStorage to persist state across pages.
 */

class MockGraphAPI {
    constructor() {
        this.delay = 800; // Simulate network latency in ms
        this._loadState();
    }

    _loadState() {
        const stored = sessionStorage.getItem('mock_graph_state');
        if (stored) {
            const state = JSON.parse(stored);
            this.isAuthenticated = state.isAuthenticated;
            this.currentUser = state.currentUser;
        } else {
            this.isAuthenticated = false;
            this.currentUser = null;
        }
    }

    _saveState() {
        sessionStorage.setItem('mock_graph_state', JSON.stringify({
            isAuthenticated: this.isAuthenticated,
            currentUser: this.currentUser
        }));
    }

    /**
     * Simulates network delay to make the experience realistic
     */
    async _simulateNetwork() {
        return new Promise(resolve => setTimeout(resolve, this.delay));
    }

    /**
     * Simulates the MSAL login process
     */
    async login() {
        await this._simulateNetwork();
        this.isAuthenticated = true;
        this.currentUser = {
            id: "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
            displayName: "Demo User",
            givenName: "Demo",
            surname: "User",
            userPrincipalName: "demo.user@m365x123456.onmicrosoft.com",
            mail: "demo.user@m365x123456.onmicrosoft.com",
            jobTitle: "Software Engineer",
            mobilePhone: "+1 555 010 9999",
            officeLocation: "123/456",
            preferredLanguage: "en-US"
        };
        this._saveState();
        return {
            accessToken: "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjF... (mock_token)",
            account: this.currentUser,
            expiresOn: new Date(new Date().getTime() + 3600 * 1000)
        };
    }

    /**
     * Simulates logout
     */
    async logout() {
        await this._simulateNetwork();
        this.isAuthenticated = false;
        this.currentUser = null;
        this._saveState();
        return true;
    }

    /**
     * GET /me
     * Retrieves the current user's profile
     */
    async getUserProfile() {
        await this._simulateNetwork();
        if (!this.isAuthenticated) throw new Error("401 Unauthorized");
        return this.currentUser;
    }

    /**
     * GET /me/messages
     * Retrieves the user's emails
     */
    async getMessages() {
        await this._simulateNetwork();
        if (!this.isAuthenticated) throw new Error("401 Unauthorized");
        
        return {
            "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users('demo.user%40m365x123456.onmicrosoft.com')/messages",
            "value": [
                {
                    "id": "AAMkADh...",
                    "createdDateTime": new Date().toISOString(),
                    "lastModifiedDateTime": new Date().toISOString(),
                    "receivedDateTime": new Date().toISOString(),
                    "hasAttachments": false,
                    "subject": "Welcome to Microsoft Graph Demo",
                    "bodyPreview": "Hi Demo User, Welcome to the Microsoft Graph API demonstration. This project showcases how to integrate various Graph services...",
                    "importance": "normal",
                    "isRead": false,
                    "sender": {
                        "emailAddress": {
                            "name": "Admin Team",
                            "address": "admin@m365x123456.onmicrosoft.com"
                        }
                    },
                    "from": {
                        "emailAddress": {
                            "name": "Admin Team",
                            "address": "admin@m365x123456.onmicrosoft.com"
                        }
                    }
                },
                {
                    "id": "BBMkADh...",
                    "createdDateTime": new Date(Date.now() - 86400000).toISOString(),
                    "lastModifiedDateTime": new Date(Date.now() - 86400000).toISOString(),
                    "receivedDateTime": new Date(Date.now() - 86400000).toISOString(),
                    "hasAttachments": true,
                    "subject": "Project Update: Q3 Goals",
                    "bodyPreview": "Please find attached the Q3 goals document. We need to review the timeline for the new feature rollout...",
                    "importance": "high",
                    "isRead": true,
                    "sender": {
                        "emailAddress": {
                            "name": "Sarah Smith",
                            "address": "sarah.s@m365x123456.onmicrosoft.com"
                        }
                    },
                    "from": {
                        "emailAddress": {
                            "name": "Sarah Smith",
                            "address": "sarah.s@m365x123456.onmicrosoft.com"
                        }
                    }
                },
                {
                    "id": "CCMkADh...",
                    "createdDateTime": new Date(Date.now() - 172800000).toISOString(),
                    "lastModifiedDateTime": new Date(Date.now() - 172800000).toISOString(),
                    "receivedDateTime": new Date(Date.now() - 172800000).toISOString(),
                    "hasAttachments": false,
                    "subject": "Coffee catch-up?",
                    "bodyPreview": "Hey, are you free for a quick coffee chat tomorrow morning? Wanted to discuss the new architecture...",
                    "importance": "low",
                    "isRead": true,
                    "sender": {
                        "emailAddress": {
                            "name": "Mike Johnson",
                            "address": "mike.j@m365x123456.onmicrosoft.com"
                        }
                    },
                    "from": {
                        "emailAddress": {
                            "name": "Mike Johnson",
                            "address": "mike.j@m365x123456.onmicrosoft.com"
                        }
                    }
                }
            ]
        };
    }

    /**
     * GET /me/events
     * Retrieves the user's calendar events
     */
    async getEvents() {
        await this._simulateNetwork();
        if (!this.isAuthenticated) throw new Error("401 Unauthorized");

        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);

        return {
            "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users('demo.user%40m365x123456.onmicrosoft.com')/events",
            "value": [
                {
                    "id": "AAMkADh...",
                    "subject": "Weekly Team Sync",
                    "bodyPreview": "Reviewing sprint progress and blockers.",
                    "start": {
                        "dateTime": new Date(today.setHours(10, 0, 0)).toISOString(),
                        "timeZone": "UTC"
                    },
                    "end": {
                        "dateTime": new Date(today.setHours(11, 0, 0)).toISOString(),
                        "timeZone": "UTC"
                    },
                    "location": {
                        "displayName": "Conference Room A"
                    },
                    "organizer": {
                        "emailAddress": {
                            "name": "Demo User",
                            "address": "demo.user@m365x123456.onmicrosoft.com"
                        }
                    },
                    "isOnlineMeeting": true,
                    "onlineMeetingProvider": "teamsMeeting"
                },
                {
                    "id": "BBMkADh...",
                    "subject": "Client Demo - Graph API",
                    "bodyPreview": "Demonstrating the new integration capabilities.",
                    "start": {
                        "dateTime": new Date(tomorrow.setHours(14, 0, 0)).toISOString(),
                        "timeZone": "UTC"
                    },
                    "end": {
                        "dateTime": new Date(tomorrow.setHours(15, 30, 0)).toISOString(),
                        "timeZone": "UTC"
                    },
                    "location": {
                        "displayName": "Microsoft Teams"
                    },
                    "organizer": {
                        "emailAddress": {
                            "name": "Sarah Smith",
                            "address": "sarah.s@m365x123456.onmicrosoft.com"
                        }
                    },
                    "isOnlineMeeting": true,
                    "onlineMeetingProvider": "teamsMeeting"
                },
                {
                    "id": "CCMkADh...",
                    "subject": "Code Review",
                    "bodyPreview": "Reviewing the PR for the authentication module.",
                    "start": {
                        "dateTime": new Date(tomorrow.setHours(16, 0, 0)).toISOString(),
                        "timeZone": "UTC"
                    },
                    "end": {
                        "dateTime": new Date(tomorrow.setHours(17, 0, 0)).toISOString(),
                        "timeZone": "UTC"
                    },
                    "location": {
                        "displayName": "Online"
                    },
                    "organizer": {
                        "emailAddress": {
                            "name": "Mike Johnson",
                            "address": "mike.j@m365x123456.onmicrosoft.com"
                        }
                    },
                    "isOnlineMeeting": false
                }
            ]
        };
    }

    /**
     * GET /me/drive/root/children
     * Retrieves files from OneDrive
     */
    async getFiles() {
        await this._simulateNetwork();
        if (!this.isAuthenticated) throw new Error("401 Unauthorized");

        return {
            "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users('demo.user%40m365x123456.onmicrosoft.com')/drive/root/children",
            "value": [
                {
                    "id": "01ABCDEF...",
                    "name": "Documents",
                    "folder": { "childCount": 12 },
                    "size": 1024000,
                    "lastModifiedDateTime": new Date(Date.now() - 3600000).toISOString(),
                    "webUrl": "https://onedrive.live.com/...",
                    "createdBy": {
                        "user": {
                            "displayName": "Demo User"
                        }
                    }
                },
                {
                    "id": "02ABCDEF...",
                    "name": "Project_Proposal.docx",
                    "file": { "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document" },
                    "size": 45032,
                    "lastModifiedDateTime": new Date(Date.now() - 7200000).toISOString(),
                    "webUrl": "https://onedrive.live.com/...",
                    "createdBy": {
                        "user": {
                            "displayName": "Demo User"
                        }
                    }
                },
                {
                    "id": "03ABCDEF...",
                    "name": "Budget_2024.xlsx",
                    "file": { "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" },
                    "size": 12500,
                    "lastModifiedDateTime": new Date(Date.now() - 86400000).toISOString(),
                    "webUrl": "https://onedrive.live.com/...",
                    "createdBy": {
                        "user": {
                            "displayName": "Sarah Smith"
                        }
                    }
                },
                {
                    "id": "04ABCDEF...",
                    "name": "Architecture_Diagram.png",
                    "file": { "mimeType": "image/png" },
                    "size": 256000,
                    "lastModifiedDateTime": new Date(Date.now() - 172800000).toISOString(),
                    "webUrl": "https://onedrive.live.com/...",
                    "createdBy": {
                        "user": {
                            "displayName": "Mike Johnson"
                        }
                    }
                }
            ]
        };
    }
}

// Export a singleton instance
const mockGraphAPI = new MockGraphAPI();
