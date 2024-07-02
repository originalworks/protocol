import { Controller, Get, Query } from '@nestjs/common'
import { AppService } from './app.service'
import { GetProofDto, GetProofResDto } from './app.dto'

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get('proof')
  async getProof(@Query() query: GetProofDto): Promise<GetProofResDto> {
    return await this.appService.getProof(query)
  }
}
