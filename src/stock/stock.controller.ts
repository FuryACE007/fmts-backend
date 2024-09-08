import { Controller, Get, Param } from '@nestjs/common';
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
}
