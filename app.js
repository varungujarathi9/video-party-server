const { Server } = require("socket.io");
const moment = require("moment-timezone");
const { v4: uuidv4 } = require("uuid");
const randomColor = require("randomcolor");

const io = new Server({
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

io.on("connection", (socket) => {
  // Create Room
  socket.on("create", (data) => {
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
    console.info(`${roomId}--room created by ${data.username}`);
    io.to(roomId).emit("created", {
      "room-id": roomId,
      "room-details": roomsDetails[roomId],
    });
  });

  // Join Existing Room
  socket.on("join", (data) => {
    const { roomId, username } = data;
    if (roomId in roomsDetails) {
      socket.join(roomId);
      roomsDetails[roomId].members[username] = randomColor(); // Assign a random color for the user
      const joinMsg = {
        senderName: "<$%^",
        message: `${username} joined the room`,
        messageNumber: messages[roomId].length + 1,
        timestamp: moment.tz("Asia/Kolkata").format("hh:mm A"),
      };
      messages[roomId].push(joinMsg);
      io.to(roomId).emit("joined", {
        username,
        "room-details": roomsDetails[roomId],
        joinMsg,
      });
      io.to(roomId).emit("update-room-details", roomsDetails[roomId]);
      console.info(`${username} joined room ${roomId}`);
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
      console.info(`Message from ${username} in room ${roomId}: ${message}`);
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
      console.info(`${username} left room ${roomId}`);
    } else {
      socket.emit("error-leaving", { message: "Error leaving the room." });
    }
  });

  socket.on("rejoin-room", (data) => {
    const roomId = data.roomID;
    if (roomsDetails[roomId]) {
      log(`${data.username} re-joined room ${roomId}`);
      messages[roomId].push({
        senderName: "<$%^",
        message: `${data.username} re-joined`,
        messageNumber: messages[roomId].length + 1,
        timestamp: moment.tz("Asia/Kolkata").format("LT"),
      });

      socket.join(roomId);
      socket.emit("update-room-details", roomsDetails[roomId]);
      socket.emit("receive_message", messages[roomId]);
    } else {
      console.log(`--room not found rejoin room -- ${roomId}`);
      socket.emit("left_room", {});
    }
  });

  socket.on("update-member-status", (data) => {
    roomsDetails[data.roomID].members[data.username] = data.ready;
    io.to(data.roomID).emit("update-room-details", roomsDetails[data.roomID]);
  });

  socket.on("start-video", (data) => {
    roomsDetails[data.room_id].started = true;
    io.to(data.room_id).emit("video-started", roomsDetails[data.room_id]);
  });

  socket.on("video-update", (data) => {
    if (data.pauseDetails.exited) {
      roomsDetails[data.pauseDetails.roomID].started = false;
    }
    io.to(data.pauseDetails.roomID).emit("updated-video", data);
  });

  socket.on("remove-member", (data) => {
    const roomId = data.roomID;
    delete roomsDetails[roomId].members[data.username];
    socket.leave(roomId);
    messages[roomId].push({
      senderName: "<$%^",
      message: `${data.username} left`,
      messageNumber: messages[roomId].length + 1,
      timestamp: moment.tz(timezone).format("LT"),
    });

    socket.emit("left_room", roomsDetails[roomId]);
    io.to(roomId).emit("update-room-details", roomsDetails[roomId]);
  });

  socket.on("remove-all-member", (data) => {
    const roomId = data.roomID;
    roomsDetails[roomId].members = {};
    roomsDetails[roomId].started = false;
    io.to(roomId).emit("all_left", roomsDetails[roomId]);
    socket.leave(roomId);
    if (Object.keys(roomsDetails[roomId].members).length === 0) {
      delete roomsDetails[roomId];
    }
  });

  socket.on("send-message", (data) => {
    data.timestamp = moment.tz("Asia/Kolkata").format("LT");
    data.messageNumber = messages[data.roomID].length + 1;
    messages[data.roomID].push(data);

    io.to(data.roomID).emit("receive_message", messages[data.roomID]);
  });

  socket.on("get-all-messages", (data) => {
    socket.emit("receive_message", messages[data.roomID]);
  });

  // webrtc socket operations
  socket.on("send-offer", (data) => {
    io.to(data.roomID).emit("receive-offer", data);
  });

  socket.on("send-answer", (data) => {
    io.to(data.roomID).emit("receive-answer", data);
  });
});

io.listen(8000);
