# 🎨 Streamlit GUI for Techline Custom Agent

A beautiful and interactive web interface for testing and demonstrating your Techline cleaning service AI assistant.

## 🚀 Quick Start

### Method 1: Auto-start both services (Windows)
```bash
start_services.bat
```

### Method 2: Auto-start both services (Unix/Linux/Mac)
```bash
chmod +x start_services.sh
./start_services.sh
```

### Method 3: Manual start
1. **Start the API server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. **Start the Streamlit GUI:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open your browser:**
   - API: http://localhost:8000
   - GUI: http://localhost:8501

## 🎯 Features

### 🏠 **Customer Experience**
- **Welcome Interface**: Clean, professional design matching Techline branding
- **Address Validation**: Real-time address/zip code validation before conversation
- **Live Chat**: Interactive chat interface with the AI assistant
- **Message Timestamps**: Track conversation flow
- **Status Indicators**: Visual feedback for validation and connection status

### 🔧 **Testing & Development**
- **API Health Check**: Monitor API server status
- **Debug Information**: View session state and thread details
- **Conversation Export**: Download full conversation data as JSON
- **Error Handling**: Comprehensive error messages and recovery options
- **Connection Management**: Easy API URL configuration for local/cloud testing

### 📊 **Business Intelligence**
- **Conversation Analytics**: View message counts and validation status
- **Thread Management**: Track individual conversation threads
- **Data Export**: Export conversation data for analysis
- **Real-time Updates**: Live conversation history fetching

## 🎨 Interface Overview

### **Sidebar Controls**
- **Start New Conversation**: Initialize a fresh conversation thread
- **Get Conversation Data**: Fetch detailed analytics and export options
- **API Configuration**: Set local or cloud API URLs
- **Health Check**: Verify API server status

### **Main Chat Area**
- **Welcome Screen**: Instructions for new users
- **Address Input**: Secure address validation form
- **Chat Interface**: Modern chat UI with role-based message styling
- **Status Messages**: Clear feedback for all user actions

### **Debug Panel** (Expandable)
- **Session Information**: Current thread ID and validation status
- **Message History**: Complete conversation flow
- **JSON Export**: Download conversation data for external analysis

## 🔄 User Flow

1. **🚀 Start**: Click "Start New Conversation" to begin
2. **📍 Validate**: Enter address or zip code for service area verification
3. **💬 Chat**: Engage with the AI assistant about cleaning needs
4. **📊 Export**: Download conversation data for business purposes

## 🛠️ Configuration

### **API URL Configuration**
- **Local Development**: `http://localhost:8000`
- **GCP Cloud Run**: `https://your-service-url.run.app`

### **Customization Options**
- **Theme Colors**: Edit `.streamlit/config.toml`
- **Branding**: Update titles and styling in `streamlit_app.py`
- **Features**: Add/remove functionality as needed

## 🎯 Use Cases

### **🧪 Development Testing**
- Test API endpoints interactively
- Validate address checking functionality
- Debug conversation flows
- Monitor assistant responses

### **📋 Demonstrations**
- Show clients the customer experience
- Present AI assistant capabilities
- Demonstrate address validation
- Showcase conversation quality

### **💼 Business Operations**
- Customer service representative tool
- Training interface for new staff
- Quality assurance testing
- Lead generation demonstrations

### **📈 Analytics & Training**
- Export conversation data for analysis
- Monitor common customer questions
- Improve assistant responses
- Track validation success rates

## 🔧 Technical Details

### **Real-time Updates**
- Uses Streamlit's session state for conversation persistence
- Automatic UI refresh after API interactions
- Error handling with user-friendly messages

### **Security Features**
- Input validation and sanitization
- Timeout protection for API calls
- Error boundary handling
- Secure data transmission

### **Performance Optimizations**
- Efficient API request handling
- Minimal UI re-rendering
- Optimized state management
- Responsive design for all devices

## 🚨 Troubleshooting

### **Common Issues**

**"Cannot connect to API"**
- Ensure the FastAPI server is running on the specified port
- Check the API URL in the sidebar configuration
- Verify firewall settings allow local connections

**"Address validation failed"**
- Check Google Maps API key configuration
- Verify internet connection for API calls
- Ensure the address format is correct

**"Chat not working"**
- Confirm address has been validated first
- Check OpenAI API key configuration
- Verify the assistant ID is correct

### **Debug Steps**
1. Use the "Check API Health" button in sidebar
2. Review debug information in expandable panel
3. Check browser console for JavaScript errors
4. Verify API server logs for backend issues

## 🎨 Customization

### **Styling**
Edit `.streamlit/config.toml` to customize:
- Primary colors
- Background colors
- Font families
- Theme settings

### **Functionality**
Modify `streamlit_app.py` to:
- Add new features
- Change UI layout
- Integrate additional APIs
- Customize business logic

## 📱 Mobile Support

The interface is responsive and works on:
- Desktop browsers
- Tablet devices
- Mobile phones
- Touch interfaces

Perfect for demonstrations on any device!
