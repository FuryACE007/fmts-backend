import { Module } from '@nestjs/common';
import { ScheduleModule } from '@nestjs/schedule';
import { StockModule } from './stock/stock.module';

@Module({
  imports: [ScheduleModule.forRoot(), StockModule],
})
export class AppModule {}
