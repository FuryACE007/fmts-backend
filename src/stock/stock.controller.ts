import {
  Controller,
  Get,
  Param,
  InternalServerErrorException,
} from '@nestjs/common';
import { StockService } from './stock.service';

@Controller('stocks')
export class StockController {
  constructor(private readonly stockService: StockService) {}

  @Get()
  getAllStocks() {
    return this.stockService.getStockData();
  }

  @Get(':symbol')
  getStock(@Param('symbol') symbol: string) {
    return this.stockService.getStockData(symbol);
  }

  @Get('historical')
  async getHistoricalData() {
    try {
      return await this.stockService.getHistoricalData();
    } catch (error) {
      console.error('Error fetching historical data:', error);
      throw new InternalServerErrorException('Failed to fetch historical data');
    }
  }
}
