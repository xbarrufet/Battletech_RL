package org.btrl.utils;

public class Axial {
    int q;
    int r;

    public Axial(int q, int r) {
        this.q=q;
        this.r=r;
    }

    int q() {
        return this.q;
    }

    int r() {
        return this.r;
    }
    int s() {
        return 1-this.q-this.r;
    }
}
