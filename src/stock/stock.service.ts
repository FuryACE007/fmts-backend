// src/stock/stock.service.ts
import { Injectable, OnModuleInit } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { spawn, ChildProcess } from 'child_process';
import { join } from 'path';

@Injectable()
export class StockService implements OnModuleInit {
  private stockData: any = {};
  private pythonProcess: ChildProcess | null = null;

  async onModuleInit() {
    await this.startPythonScript();
  }

  private async startPythonScript(): Promise<void> {
    return new Promise((resolve) => {
      const pythonScriptPath = join(
        __dirname,
        '..',
        '..',
        'python',
        'stock_data_fetcher.py',
      );
      this.pythonProcess = spawn('python', [pythonScriptPath]);

      let dataBuffer = '';

      this.pythonProcess.stdout.on('data', (data) => {
        dataBuffer += data.toString();

        // Attempt to parse JSON when a newline is detected
        if (dataBuffer.includes('\n')) {
          try {
            const parsedData = JSON.parse(dataBuffer);
            this.updateStockData(parsedData);
            dataBuffer = ''; // Clear the buffer after successful parsing
          } catch (error) {
            console.error('Error parsing Python script output:', error);
          }
        }
      });

      this.pythonProcess.stderr.on('data', (data) => {
        console.error(`Python script error: ${data}`);
      });

      this.pythonProcess.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        this.pythonProcess = null;
        if (code !== 0) {
          this.startPythonScript();
        }
      });

      resolve();
    });
  }

  private updateStockData(newData: any): void {
    newData.forEach((stock: any) => {
      this.stockData[stock.Symbol] = stock;
    });
    console.log('Stock data updated:', Object.keys(newData).length, 'symbols');
  }

  @Cron(CronExpression.EVERY_HOUR)
  async checkPythonScript() {
    if (!this.pythonProcess) {
      console.log('Python script not running. Restarting...');
      await this.startPythonScript();
    } else {
      console.log('Python script is running correctly.');
    }
  }

  getStockData(symbol?: string): any {
    if (symbol) {
      return this.stockData[symbol] || null;
    }
    return this.stockData;
  }
}
