package org.btrl.model;

import org.btrl.utils.Axial;
import org.btrl.utils.BattletechRLException;

import java.util.HashMap;
import java.util.Map;

public class BoardImp {
    int width;
    int height;
    Map<Axial,Cell> cells;

    BoardImp(int width, int height, String[] cell_str_list) throws Exception {
        this.width=width;
        this.height = height;
        this.cells = this.build_cells_map(width,height,cell_str_list);
    }

    private Map<Axial, Cell> build_cells_map(int width, int height, String[] cell_str_list) throws Exception {
        Map<Axial, Cell> cells = new HashMap<Axial, Cell>();
        int cells_counter = 0;
        try {
            for(int i=0;i<this.width;i++) {
                int r = i;
                for(int q=0;q<this.width;q++) {
                    if(q>0 & q%2==0) {
                        r--;
                    }
                    String cell_str = cell_str_list[cells_counter++];
                    Axial position = new Axial(q,r);
                    CellType cellType = CellType.valueOf(Integer.parseInt(cell_str.substring(1)));
                    cells.put(position, new Cell(position,cellType));
                }

            }
        } catch (Exception e) {
            throw new BattletechRLException("Error parsing board",e);
        }
        return  cells;

    }

}
