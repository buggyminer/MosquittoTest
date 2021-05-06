package com.megrx.java;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;


public class Util {

    public static void main(String[] args) {
        System.out.println(byteArrayInBinary("will msg".getBytes(StandardCharsets.UTF_8)));
    }

    /**
     * Encode UTF-8 String according to Section 1.5.3
     * @param list
     * @param string
     */
    public static void encodeUTF8String(List<Byte> list, String string) {
        int msb;
        int lsb;
        int length = string.length();
        msb = length / 256;
        lsb = length % 256;
        list.add((byte)msb);
        list.add((byte)lsb);
        if (length > 0) {
            for (byte b : string.getBytes(StandardCharsets.UTF_8)) {
                list.add(b);
            }
        }
    }

    /**
     * encode the length of Remaining Length field in fixed header
     * @param length the length(int) to be encoded
     * @return the encoded length(byte[])
     */
    public static List<Byte> encodeLength(int length) {
        List<Byte> result = new ArrayList<>();
        Byte encodedByte;
        do {
            encodedByte = (byte)(length % 128);
            length /= 128;
            if (length > 0)
                encodedByte = setBit(encodedByte, 7);
            result.add(encodedByte);
        } while (length > 0);
        return result;
    }

    /**
     * decode the length of Remaining Length field in fixed header
     * @param bytes the length(byte[]) to be decoded
     * @return the decoded length(int)
     */
    public static int decodeLength(List<Byte> bytes) {
        int result = 0;
        int multiplier = 1;
        for (byte b : bytes) {
            result += (b & 127) * multiplier;
            multiplier *= 128;
            if (multiplier > 128 * 128 * 128)
                throw new RuntimeException("Malformed Remaining Length");
        }
        return result;
    }

    /**
     * A byte consists of 8 bits, whose indexes from left to right are 7,6,...,1,0
     * This function set the bit of byte `b` in index `pos` to 1
     * @param b     the byte to be set
     * @param pos   the index of bit to be set
     * @return      the resulted byte
     */
    public static byte setBit(byte b, int pos) {
        return b |= (1 << pos);
    }

    /**
     * A byte consists of 8 bits, whose indexes from left to right are 7,6,...,1,0
     * This function clear the bit of byte `b` in index `pos` to 0
     * @param b     the byte to be clear
     * @param pos   the index of bit to be clear
     * @return      the resulted byte
     */
    public static byte clearBit(byte b, int pos) {
        return b &= ~(1 << pos);
    }

    /**
     * treat `b` as a unsigned byte, return its value in int representation
     * @param b a unsigned byte
     * @return unsigned byte's int value
     */
    public static int unsignedByteToInt(byte b) {
        return b & 0xFF;
    }

    /**
     * return `i` in unsigned byte representation
     * @param i an integer
     * @return `i` in unsigned byte representation
     */
    public static byte intToUnsignedByte(int i) {
        return (byte)i;
    }

    /**
     * @param b
     * @return 'b' in heximal representation
     */
    public static String byteInHeximal(byte b) {
        return String.format("%02X", b);
    }

    /**
     * @param b
     * @return 'b' in binary representation
     */
    public static String byteInBinary(byte b) {
        return String.format("%8s", Integer.toBinaryString(b & 0xFF)).replace(' ', '0');
    }

    /**
     * return byte array `ba` in heximal representation
     * each byte occupies one line
     * @param ba
     * @return a heximal string of `ba`
     */
    public static String byteArrayInHeximal(byte[] ba) {
        StringBuilder sb = new StringBuilder();
        for (byte b : ba) {
            sb.append(byteInHeximal(b));
            sb.append("\n");
        }
        return sb.toString();
    }

    /**
     * return byte array `ba` in binary representation
     * each byte occupies one line
     * @param ba
     * @return a binary string of `ba`
     */
    public static String byteArrayInBinary(byte[] ba) {
        StringBuilder sb = new StringBuilder();
        for (byte b : ba) {
            sb.append(byteInBinary(b));
            sb.append("\n");
        }
        return sb.toString();
    }

    /**
     * return byte array `ba` in binary representation
     * each byte occupies one line
     * each line is prefixed with a line number (started from 1)
     * @param ba
     * @return a binary string of `ba`
     */
    public static String byteArrayInBinaryWithIndex(byte[] ba) {
        StringBuilder sb = new StringBuilder();
        int index = 1;
        for (byte b : ba) {
            sb.append(String.format("%02d: ", index++));
            sb.append(byteInBinary(b));
            sb.append("\n");
        }
        return sb.toString();
    }
}
