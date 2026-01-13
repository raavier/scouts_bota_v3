"""
Data Loader Component
Handles loading and saving of base_peso.xlsx with backup system
"""

import pandas as pd
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional
import streamlit as st


class DataLoader:
    """Manages loading and saving of weight data"""

    def __init__(self):
        """Initialize paths"""
        # Get base directory (parent of streamlit_app)
        self.base_dir = Path(__file__).parent.parent.parent

        # Define paths
        self.inputs_dir = self.base_dir / "bases" / "inputs"
        self.business_dir = self.inputs_dir / "business"
        self.weights_file = self.business_dir / "base_peso.xlsx"
        self.backup_dir = self.business_dir / "backups"

        # Create directories if they don't exist
        self.business_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def load_weights(self) -> Optional[pd.DataFrame]:
        """
        Load weights file from Excel

        Returns:
            pd.DataFrame if file exists and loads successfully, None otherwise
        """
        try:
            if not self.weights_file.exists():
                st.error(f"❌ Arquivo não encontrado: {self.weights_file}")
                st.info("💡 Coloque o arquivo base_peso.xlsx em: bases/inputs/business/")
                return None

            df = pd.read_excel(self.weights_file)

            # Validate basic structure
            if "INDICADOR" not in df.columns:
                st.error("❌ Arquivo inválido: coluna 'INDICADOR' não encontrada")
                return None

            return df

        except Exception as e:
            st.error(f"❌ Erro ao carregar arquivo: {str(e)}")
            return None

    def save_weights(self, df: pd.DataFrame, create_backup: bool = True) -> bool:
        """
        Save weights DataFrame to Excel

        Args:
            df: DataFrame to save
            create_backup: Whether to create backup before saving

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create backup if requested and file exists
            if create_backup and self.weights_file.exists():
                backup_path = self._create_backup()
                if backup_path:
                    st.success(f"✅ Backup criado: {backup_path.name}")

            # Save to Excel
            df.to_excel(self.weights_file, index=False, engine='openpyxl')

            return True

        except Exception as e:
            st.error(f"❌ Erro ao salvar arquivo: {str(e)}")
            return False

    def _create_backup(self) -> Optional[Path]:
        """
        Create timestamped backup of current weights file

        Returns:
            Path to backup file if successful, None otherwise
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"base_peso_backup_{timestamp}.xlsx"

            shutil.copy2(self.weights_file, backup_file)

            return backup_file

        except Exception as e:
            st.warning(f"⚠️ Erro ao criar backup: {str(e)}")
            return None

    def list_backups(self) -> list:
        """
        List all backup files

        Returns:
            List of backup file paths, sorted by modification time (newest first)
        """
        backups = list(self.backup_dir.glob("base_peso_backup_*.xlsx"))
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return backups

    def restore_backup(self, backup_file: Path) -> bool:
        """
        Restore weights from a backup file

        Args:
            backup_file: Path to backup file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create backup of current file before restoring
            if self.weights_file.exists():
                self._create_backup()

            # Copy backup to main file
            shutil.copy2(backup_file, self.weights_file)

            return True

        except Exception as e:
            st.error(f"❌ Erro ao restaurar backup: {str(e)}")
            return False

    def create_sample_file(self) -> bool:
        """
        Create a sample base_peso.xlsx file for testing

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            from ..utils.constants import POSITION_LIST

            # Sample data
            sample_data = {
                "INDICADOR": [
                    "Passes Attempted",
                    "Passes Completed",
                    "Tackles",
                    "Interceptions",
                    "Shots",
                    "Goals"
                ],
                "CLASSIFICACAO RANKING": [
                    "PASS",
                    "PASS",
                    "DEFENSIVE",
                    "DEFENSIVE",
                    "OFFENSIVE",
                    "OFFENSIVE"
                ],
                "SUBCLASSIFICACAO RANKING": [
                    "Progressive Passing",
                    "Progressive Passing",
                    "Defending",
                    "Defending",
                    "Shooting",
                    "Shooting"
                ],
                "CONSIDERAR?": ["SIM"] * 6,
                "ESPECIAL?": [""] * 6,
                "Melhor para": ["CIMA"] * 6,
                "tipo_agreg": ["sum"] * 6,
                "Explicação indicador": [
                    "Número de passes tentados",
                    "Número de passes completos",
                    "Número de desarmes",
                    "Número de interceptações",
                    "Número de chutes",
                    "Número de gols"
                ]
            }

            # Add position columns with sample weights
            for pos in POSITION_LIST:
                if pos == "GK":
                    sample_data[pos] = [10, 10, 5, 10, 5, 5]
                elif pos in ["CB", "RCB", "LCB"]:
                    sample_data[pos] = [60, 65, 90, 85, 20, 15]
                elif pos in ["RB", "LB"]:
                    sample_data[pos] = [70, 75, 80, 75, 30, 20]
                elif pos == "DM":
                    sample_data[pos] = [80, 85, 85, 80, 35, 25]
                elif pos == "CM":
                    sample_data[pos] = [85, 90, 70, 70, 50, 40]
                elif pos == "AM":
                    sample_data[pos] = [80, 85, 50, 50, 75, 65]
                elif pos in ["LW", "RW"]:
                    sample_data[pos] = [70, 75, 40, 45, 85, 75]
                elif pos == "CF":
                    sample_data[pos] = [60, 65, 30, 35, 95, 90]

            df = pd.DataFrame(sample_data)
            df.to_excel(self.weights_file, index=False, engine='openpyxl')

            return True

        except Exception as e:
            st.error(f"❌ Erro ao criar arquivo de exemplo: {str(e)}")
            return False
