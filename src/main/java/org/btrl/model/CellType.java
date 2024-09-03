package org.btrl.model;
import java.util.Map;
import java.util.HashMap;

public enum CellType {
    plain(0), light_forest(1), heavy_forest(2);

    final private int value;
    final private static Map<Integer, CellType> map = new HashMap<Integer, CellType>();

    private CellType(int value) {
        this.value = value;
    }

    static {
        for (CellType pageType : CellType.values()) {
            map.put(pageType.value, pageType);
        }
    }

    public static CellType valueOf(int pageType) {
        return (CellType) map.get(pageType);
    }

    public int getValue() {
        return value;
    }
}