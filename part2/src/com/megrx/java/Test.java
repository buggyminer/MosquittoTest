package com.megrx.java;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Arrays;

public class Test {

    private static String host = "localhost";
    private static int port = 1883;     // default port of mosquitto server
    private static int bufferSize = 8 * 1024;
    private static Socket socket;
    private static InputStream input;
    private static OutputStream output;

    public static void main(String[] args) {
        testCase01();
    }

    /**
     * this function do the following things:
     *  1. establish connection with mosquitto
     *  2. send a CONNECT packet
     *  3. receive the response from mosquitto
     * BUG: `Socket error on client gwan, disconnecting.`
     * @param config
     */
    static void execute(ConnectPacketConfig config) {
        // create packet instance
        ConnectPacket packet = new ConnectPacket(config);

        // get packet byte array
        byte[] data = packet.get();
        System.out.println("###############CONNECT###############");
        System.out.println(Util.byteArrayInBinaryWithIndex(data));

        // create connection
        try {
            socket = new Socket(host, port);
        } catch (IOException e) {
            System.out.println("Can't establish TCP connection");
            e.printStackTrace();
        }

        try {
            input = socket.getInputStream();
            output = socket.getOutputStream();

            // send packet
            output.write(data);
            output.flush();

            // receive response
            byte[] response = new byte[bufferSize];
            int byteRead = input.read(response);
            response = Arrays.copyOfRange(response, 0, byteRead);
            System.out.println("###############CONNACK###############");
            System.out.println(Util.byteArrayInBinaryWithIndex(response));
        } catch (IOException e) {
            System.out.println("I/O Error");
            e.printStackTrace();
        } finally {
            try {
                output.close();
                input.close();
                socket.close();
            } catch (IOException e) {
                System.out.println("Can't close stream or socket properly");
                e.printStackTrace();
            }
        }
    }

    static void testCase01() {
        // create configuration instance
        ConnectPacketConfig config = new ConnectPacketConfig();
        // config here
        config.usernameFlag = false;
        config.passwordFlag = false;
        config.willRetain = false;
        config.willQOS = 1;
        config.willFlag = true;
        config.cleanSession = true;
        config.keepAlive = 0;
        config.clientID = "gwan";
        config.willTopic = "test";
        config.willMessage = "will msg";
        config.username = "un";
        config.password = "pw";

        execute(config);
    }
}
