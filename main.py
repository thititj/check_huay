import json
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

# สร้าง FastAPI instance
app = FastAPI(
    title="Thai Lottery API",
    description="API สำหรับตรวจผลสลากกินแบ่งรัฐบาล",
    version="1.0.0"
)

class TicketRequest(BaseModel):
    ticket_number: str = Field(..., min_length=6, max_length=6, description="หมายเลขสลากที่ต้องการตรวจ (6 หลัก)")

class CheckResult(BaseModel):
    ticket_number: str
    is_winning: bool
    message: str
    prizes: List[str] = []
    total_amount: int = 0
    total_amount_text: str = ""

def number_to_thai_text(number):
    """
    แปลงตัวเลขเป็นคำอ่านภาษาไทย
    
    Parameters:
    number (int): จำนวนเงินที่ต้องการแปลง
    
    Returns:
    str: คำอ่านภาษาไทยของจำนวนเงิน
    """
    # ตัวเลขหลัก
    thai_digits = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
    # หลักเลข
    thai_units = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
    
    if number == 0:
        return "ศูนย์"
    
    # กรณีจำนวนเงินมากกว่าล้าน
    if number >= 1000000:
        million_part = number // 1000000
        remainder = number % 1000000
        
        result = number_to_thai_text(million_part) + "ล้าน"
        
        if remainder > 0:
            result += number_to_thai_text(remainder)
        
        return result
    
    # แปลงตัวเลขเป็นสตริง
    num_str = str(number)
    
    result = ""
    for i, digit in enumerate(num_str):
        position = len(num_str) - i - 1
        if digit == '0':
            continue
            
        # กรณีพิเศษสำหรับเลข 1 ในหลักสิบ
        if position == 1 and digit == '1':
            result += "สิบ"
        # กรณีพิเศษสำหรับเลข 2 ในหลักสิบ
        elif position == 1 and digit == '2':
            result += "ยี่สิบ"
        # กรณีพิเศษสำหรับเลข 1 ในหลักหน่วย
        elif position == 0 and digit == '1' and len(num_str) > 1:
            result += "เอ็ด"
        else:
            result += thai_digits[int(digit)] + thai_units[position]
    
    return result

def get_lottery_data():
    """
    โหลดข้อมูลรางวัลสลากกินแบ่งรัฐบาล
    
    Returns:
    dict: ข้อมูลผลการออกรางวัลสลากกินแบ่งรัฐบาล
    """
    try:
        with open('lottery_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # ข้อมูลตัวอย่างในกรณีที่ไม่มีไฟล์
        return {
            "drawDate": "2024-03-16",
            "prizes": {
                "first": {"number": "757563", "amount": 6000000, "count": 1},
                "neighboring": {"numbers": ["757562", "757564"], "amount": 100000, "count": 2},
                "front3": {"numbers": ["595", "927"], "amount": 4000, "count": 2},
                "last3": {"numbers": ["457", "309"], "amount": 4000, "count": 2},
                "last2": {"numbers": ["32"], "amount": 2000, "count": 1},
                "second": {"numbers": ["989893", "041134", "465815", "875925", "748827"], "amount": 200000, "count": 5},
                "third": {
                    "numbers": ["571016", "750873", "472259", "455376", "633053", "139119", "141267", "347605", "246223", "909970"],
                    "amount": 80000, "count": 10
                },
                "fourth": {
                    "numbers": [
                        "853348", "802025", "865801", "074040", "248923", "209713", "247158", "116520", "532411", "415164",
                        "342135", "492265", "124537", "964672", "113275", "572952", "074509", "347176", "252613", "231327",
                        "649727", "856757", "579180", "427466", "168423", "544466", "546436", "205246", "120687", "519010",
                        "661839", "344622", "782028", "883412", "466815", "175231", "214933", "395960", "369661", "961506",
                        "122064", "830000", "468063", "295987", "262297", "874836", "566906", "636983", "408506", "824008"
                    ],
                    "amount": 40000, "count": 50
                },
                "fifth": {
                    "numbers": [
                        "930065", "051805", "933952", "755320", "907596", "094743", "440097", "164129", "133740", "795591",
                        "348500", "547511", "205399", "915106", "233255", "632802", "138684", "042591", "318762", "011186",
                        "573421", "841412", "430316", "988703", "914448", "954469", "032771", "532065", "684442", "793479",
                        "920930", "969472", "735763", "563666", "876311", "915765", "268658", "225984", "915506", "375607",
                        "498114", "316228", "426624", "034665", "782761", "588685", "599129", "907523", "642669", "992720",
                        "664304", "483655", "458447", "964766", "692681", "158520", "953027", "366349", "937521", "456950",
                        "983847", "028135", "606555", "961105", "313132", "374805", "877480", "526740", "221239", "124954",
                        "997455", "047836", "084790", "572339", "240622", "580626", "039933", "859329", "080656", "627079",
                        "195765", "687423", "488862", "473219", "134502", "160909", "029268", "409757", "004058", "204243",
                        "981958", "275463", "532573", "981550", "016450", "109999", "293176", "372464", "110149", "348438"
                    ],
                    "amount": 20000, "count": 100
                }
            }
        }

def check_lottery(ticket_number: str, lottery_data: Dict[str, Any]) -> CheckResult:
    """
    ตรวจผลสลากกินแบ่งรัฐบาล
    
    Parameters:
    ticket_number (str): หมายเลขสลากที่ต้องการตรวจ
    lottery_data (dict): ข้อมูลผลการออกรางวัลสลากกินแบ่งรัฐบาล
    
    Returns:
    CheckResult: ผลการตรวจสลาก
    """
    # ตรวจสอบว่าเลขสลากครบ 6 หลักหรือไม่
    if len(ticket_number) != 6:
        raise HTTPException(status_code=400, detail=f"เราได้รับหมายเลขเพียงแค่ {len(ticket_number)} หลัก กรุณาทำรายการใหม่อีกครั้ง")
    
    # เตรียมตัวแปรสำหรับเก็บผลการตรวจสลาก
    winning_results = []
    total_prize_amount = 0
    
    # ตรวจรางวัลที่ 1
    if ticket_number == lottery_data["prizes"]["first"]["number"]:
        amount = lottery_data["prizes"]["first"]["amount"]
        winning_results.append("ถูกรางวัลที่ 1")
        total_prize_amount += amount
    
    # ตรวจรางวัลเลขข้างเคียงรางวัลที่ 1
    if ticket_number in lottery_data["prizes"]["neighboring"]["numbers"]:
        amount = lottery_data["prizes"]["neighboring"]["amount"]
        winning_results.append("ถูกรางวัลข้างเคียงรางวัลที่ 1")
        total_prize_amount += amount
    
    # ตรวจรางวัลที่ 2
    if ticket_number in lottery_data["prizes"]["second"]["numbers"]:
        amount = lottery_data["prizes"]["second"]["amount"]
        winning_results.append("ถูกรางวัลที่ 2")
        total_prize_amount += amount
    
    # ตรวจรางวัลที่ 3
    if ticket_number in lottery_data["prizes"]["third"]["numbers"]:
        amount = lottery_data["prizes"]["third"]["amount"]
        winning_results.append("ถูกรางวัลที่ 3")
        total_prize_amount += amount
    
    # ตรวจรางวัลที่ 4
    if ticket_number in lottery_data["prizes"]["fourth"]["numbers"]:
        amount = lottery_data["prizes"]["fourth"]["amount"]
        winning_results.append("ถูกรางวัลที่ 4")
        total_prize_amount += amount
    
    # ตรวจรางวัลที่ 5
    if ticket_number in lottery_data["prizes"]["fifth"]["numbers"]:
        amount = lottery_data["prizes"]["fifth"]["amount"]
        winning_results.append("ถูกรางวัลที่ 5")
        total_prize_amount += amount
    
    # ตรวจเลขหน้า 3 ตัว
    first_three_digits = ticket_number[:3]
    if first_three_digits in lottery_data["prizes"]["front3"]["numbers"]:
        amount = lottery_data["prizes"]["front3"]["amount"]
        winning_results.append("ถูกรางวัลเลขหน้า 3 ตัว")
        total_prize_amount += amount
    
    # ตรวจเลขท้าย 3 ตัว
    last_three_digits = ticket_number[-3:]
    if last_three_digits in lottery_data["prizes"]["last3"]["numbers"]:
        amount = lottery_data["prizes"]["last3"]["amount"]
        winning_results.append("ถูกรางวัลเลขท้าย 3 ตัว")
        total_prize_amount += amount
    
    # ตรวจเลขท้าย 2 ตัว
    last_two_digits = ticket_number[-2:]
    if last_two_digits in lottery_data["prizes"]["last2"]["numbers"]:
        amount = lottery_data["prizes"]["last2"]["amount"]
        winning_results.append("ถูกรางวัลเลขท้าย 2 ตัว")
        total_prize_amount += amount
    
    # สรุปผลการตรวจรางวัล
    if winning_results:
        message = f"ยินดีด้วย หมายเลข {ticket_number} ของคุณ "
        
        # สร้างข้อความแสดงรางวัลที่ถูกพร้อมคำว่า "และ" คั่นระหว่างรางวัลสุดท้าย
        if len(winning_results) == 1:
            message += winning_results[0]
        else:
            # เพิ่มคำว่า "และ" ก่อนรางวัลสุดท้าย
            formatted_results = winning_results[:-1]
            formatted_results.append("และ" + winning_results[-1][3:])  # ตัด "ถูก" ออกจากรางวัลสุดท้าย
            
            # รวมรางวัลทั้งหมดโดยมีคำว่า "และ" ก่อนรางวัลสุดท้าย
            message += " ".join(formatted_results)
        
        total_prize_text = number_to_thai_text(total_prize_amount) + "บาท"
        message += f" รวมเป็นเงินทั้งสิ้น {total_prize_text}"
        
        return CheckResult(
            ticket_number=ticket_number,
            is_winning=True,
            message=message,
            prizes=winning_results,
            total_amount=total_prize_amount,
            total_amount_text=total_prize_text
        )
    else:
        return CheckResult(
            ticket_number=ticket_number,
            is_winning=False,
            message=f"หมายเลข {ticket_number} ไม่ถูกรางวัล ขอแสดงความเสียใจด้วยค่ะ"
        )

@app.get("/")
def read_root():
    return {"message": "ยินดีต้อนรับสู่ API ตรวจผลสลากกินแบ่งรัฐบาล", "version": "1.0.0"}

# เพิ่ม endpoints สำหรับ health check ตามที่ต้องการ
@app.get("/check", status_code=status.HTTP_200_OK)
def health_check():
    """
    Health check endpoint ที่คืนค่าสถานะ 200 OK
    สำหรับใช้กับ cron job เพื่อป้องกันไม่ให้ service หลับใน Render
    """
    return Response(status_code=status.HTTP_200_OK)

@app.get("/heart-beat", status_code=status.HTTP_200_OK)
def heart_beat():
    """
    อีก endpoint สำหรับ health check ที่คืนค่าสถานะ 200 OK
    สำหรับใช้กับ cron job เพื่อป้องกันไม่ให้ service หลับใน Render
    """
    return Response(status_code=status.HTTP_200_OK)

@app.get("/lottery/info")
def get_lottery_info():
    """
    ข้อมูลงวดล่าสุดของสลากกินแบ่งรัฐบาล
    """
    lottery_data = get_lottery_data()
    return {
        "drawDate": lottery_data["drawDate"],
        "first_prize": lottery_data["prizes"]["first"]["number"]
    }

@app.post("/lottery/check", response_model=CheckResult)
def check_ticket(request: TicketRequest):
    """
    ตรวจผลสลากกินแบ่งรัฐบาล
    """
    lottery_data = get_lottery_data()
    return check_lottery(request.ticket_number, lottery_data)

# สำหรับรัน server แบบ local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)