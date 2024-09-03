package org.btrl.utils;

public class BattletechRLException extends Exception {

    public BattletechRLException(String msg, Exception e) {
        super(msg,e);
    }

    public BattletechRLException(String msg) {
        super(msg);
    }

    public BattletechRLException(Exception e) {
        super(e);
    }
}
