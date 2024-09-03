package org.btrl.model;

import org.btrl.utils.Axial;

public class Cell {

        Axial position;
        CellType cellType;
        String mechId;

        Cell(Axial position, CellType cellType) {
                this.cellType=cellType;
                this.position=position;
                this.mechId=null;
        }

        public Axial getPosition() {
                return position;
        }


        public CellType getCellType() {
                return cellType;
        }

        public boolean isOccupied() {
                return this.mechId == null;
        }

        public void removeMech() {
                this.mechId = null;
        }

        public void deployMech(String mechId) {
                this.mechId = mechId;
        }

        public String getMechId() {
                return mechId;
        }
}

