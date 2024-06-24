const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const moment = require("moment-timezone");
const { v4: uuidv4 } = require("uuid");
const randomColor = require("randomcolor"); // For generating random avatar colors
const winston = require("winston");

// Setup logger
const logger = winston.createLogger({
  level: "info",
  format: winston.format.simple(),
  transports: [new winston.transports.File({ filename: "record.log" })],
});

// Initialize Express and HTTP server
const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
  },
});

// Global variables
const roomsDetails = {};
const messages = {};

// Utility function to generate room ID
function getRoomId(length) {
  let result = "";
  const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  const charactersLength = characters.length;
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

// Socket.io connection
io.on("connection", (socket) => {
  logger.info("socket is connected");

  socket.on("disconnect", () => {
    logger.info("server is disconnected");
  });

  socket.on("create-room", (data) => {
    let roomId = getRoomId(6);
    while (roomsDetails[roomId]) {
      roomId = getRoomId(6);
    }
    const createdAt = moment.tz("Asia/Kolkata").format("MM/DD/YY @ HH:mm:ss");
    roomsDetails[roomId] = {
      members: { [data.username]: randomColor() },
      createdAt,
      started: false,
    };
    messages[roomId] = [];
    messages[roomId].push({
      senderName: "<$%^",
      message: `${data.username} created room`,
      messageNumber: messages[roomId].length + 1,
      timestamp: moment.tz("Asia/Kolkata").format("hh:mm A"),
    });

    socket.join(roomId);
    logger.info(`${roomId}--room created by ${data.username}`);
    io.to(roomId).emit("room-created", {
      "room-id": roomId,
      "room-details": roomsDetails[roomId],
    });
  });

  // Join-room event handler
  socket.on("join-room", (data) => {
    const { roomId, username } = data;
    if (roomsDetails[roomId]) {
      socket.join(roomId);
      roomsDetails[roomId].members[username] = randomColor(); // Assign a random color for the user
      const joinMsg = {
        senderName: "<$%^",
        message: `${username} joined the room`,
        messageNumber: messages[roomId].length + 1,
        timestamp: moment.tz("Asia/Kolkata").format("hh:mm A"),
      };
      messages[roomId].push(joinMsg);
      io.to(roomId).emit("user-joined", {
        username,
        "room-details": roomsDetails[roomId],
        joinMsg,
      });
      logger.info(`${username} joined room ${roomId}`);
    } else {
      socket.emit("error-joining", { message: "Room does not exist." });
    }
  });

  // Send-message event handler
  socket.on("send-message", (data) => {
    const { roomId, message, username } = data;
    if (roomsDetails[roomId]) {
      const msg = {
        senderName: username,
        message: message,
        messageNumber: messages[roomId].length + 1,
        timestamp: moment.tz("Asia/Kolkata").format("hh:mm A"),
      };
      messages[roomId].push(msg);
      io.to(roomId).emit("new-message", msg);
      logger.info(`Message from ${username} in room ${roomId}: ${message}`);
    } else {
      socket.emit("error-sending", { message: "Room does not exist." });
    }
  });

  // Leave-room event handler
  socket.on("leave-room", (data) => {
    const { roomId, username } = data;
    if (roomsDetails[roomId] && roomsDetails[roomId].members[username]) {
      socket.leave(roomId);
      delete roomsDetails[roomId].members[username];
      const leaveMsg = {
        senderName: "<$%^",
        message: `${username} left the room`,
        messageNumber: messages[roomId].length + 1,
        timestamp: moment.tz("Asia/Kolkata").format("hh:mm A"),
      };
      messages[roomId].push(leaveMsg);
      io.to(roomId).emit("user-left", {
        username,
        "room-details": roomsDetails[roomId],
        leaveMsg,
      });
      logger.info(`${username} left room ${roomId}`);
    } else {
      socket.emit("error-leaving", { message: "Error leaving the room." });
    }
  });

  // Handling socket disconnection
  socket.on("disconnect", () => {
    logger.info("User disconnected");
  });
});

// Start the server
const PORT = process.env.PORT || 5000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
