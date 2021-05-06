package com.megrx.java;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;

public class ConnectPacket {

    private ConnectPacketConfig config;
    private byte[] result = null;

    public ConnectPacket(ConnectPacketConfig config) {
        this.config = config;
    }

    /**
     * @return the CONNECT packet in byte array representation
     */
    public byte[] get() {
        if (result != null)
            return result;

        int remainingLength;
        byte b1 = 0;
        List<Byte> fixedHeader;
        List<Byte> variableHeader;
        List<Byte> payload;
        ByteArrayOutputStream output = new ByteArrayOutputStream();

        // variable header
        variableHeader = variableHeader();

        // payload
        payload = payload();

        // length of variable header and payload
        remainingLength = variableHeader.size() + payload.size();

        // fixed header
        b1 = Util.setBit(b1, 4);
        fixedHeader = fixedHeader(b1, remainingLength);

        // write each array to output stream
        for (byte b : fixedHeader)      output.write(b);
        for (byte b : variableHeader)   output.write(b);
        for (byte b : payload)          output.write(b);

        // get byte array
        result = output.toByteArray();
        return result;
    }

    /**
     * make a fixed header
     * @param b1 the first byte of fixed header
     * @param remainingLength the Remaining Length field
     * @return the fixed header(byte[])
     */
    public static List<Byte> fixedHeader(byte b1, int remainingLength) {
        List<Byte> result = new ArrayList<>();

        result.add(b1);

        List<Byte> lengthByteList = Util.encodeLength(remainingLength);
        result.addAll(lengthByteList);

        return result;
    }

    /**
     * used only by get()
     * @return the variable header
     */
    private List<Byte> variableHeader() {
        List<Byte> result = new ArrayList<>();
        int msb;
        int lsb;

        // Protocol Name
        msb = 0;
        lsb = 4;
        result.add(Util.intToUnsignedByte(msb));
        result.add(Util.intToUnsignedByte(lsb));
        result.add((byte)'M');
        result.add((byte)'Q');
        result.add((byte)'T');
        result.add((byte)'T');

        // Protocol Level
        result.add((byte)4);

        // Connect Flags
        byte connect = 0;
        if (config.cleanSession) connect = Util.setBit(connect, 1);
        if (config.willFlag) connect = Util.setBit(connect, 2);
        if (config.willQOS % 2 == 1) connect = Util.setBit(connect, 3);
        if (config.willQOS / 2 == 1) connect = Util.setBit(connect, 4);
        if (config.willRetain) connect = Util.setBit(connect, 5);
        if (config.passwordFlag) connect = Util.setBit(connect, 6);
        if (config.usernameFlag) connect = Util.setBit(connect, 7);
        result.add(connect);

        // Keep Alive
        msb = config.keepAlive / 256;
        lsb = config.keepAlive % 256;
        result.add(Util.intToUnsignedByte(msb));
        result.add(Util.intToUnsignedByte(lsb));

        return result;
    }

    /**
     * used only by get()
     * @return the payload
     */
    private List<Byte> payload() {
        List<Byte> result = new ArrayList<>();
        int msb;
        int lsb;

        // Client Identifier
        Util.encodeUTF8String(result, config.clientID);

        // Will Topic
        if (config.willFlag) {
            Util.encodeUTF8String(result, config.willTopic);
        }

        // Will Message
        if (config.willFlag) {
            Util.encodeUTF8String(result, config.willMessage);
        }

        // User Name
        if (config.usernameFlag) {
            Util.encodeUTF8String(result, config.username);
        }

        // Password
        if (config.passwordFlag) {
            Util.encodeUTF8String(result, config.password);
        }

        return result;
    }
}
