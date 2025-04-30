from datetime import datetime, timedelta

employees = []
daily_records = []

def add_employee():
    name = input("请输入员工姓名：").strip()
    if name in employees:
        print("员工已存在。")
    else:
        employees.append(name)
        print(f"员工 {name} 添加成功。")

def remove_ployee():
    name = input("请输入要删除的员工姓名：").strip()
    if name in employees:
        employees.remove(name)
        print(f"员工 {name} 删除成功。")
    else:
        print("员工不存在于当前列表中。")

def input_daily_data():
    date_str = input("请输入日期（YYYY-MM-DD）：").strip()
    
    # 检查日期是否已存在
    for record in daily_records:
        if record['date'] == date_str:
            print("该日期已存在，请先删除原记录。")
            return
    
    hours_dict = {}
    while True:
        print("\n当前可选员工：", ', '.join(employees) if employees else "无")
        name = input("输入员工姓名（留空结束添加）：").strip()
        if not name:
            break
        if name not in employees:
            print("该员工不在当前列表中，请重新输入。")
            continue
        
        # 选择输入方式
        method = input("选择工时输入方式：1. 开始/结束时间 2. 直接输入工时：").strip()
        hours = 0
        if method == '1':
            try:
                start_str = input("输入开始时间（HH:MM）：").strip()
                end_str = input("输入结束时间（HH:MM）：").strip()
                start = datetime.strptime(start_str, "%H:%M")
                end = datetime.strptime(end_str, "%H:%M")
                if end < start:
                    end += timedelta(days=1)
                delta = end - start
                hours = delta.total_seconds() / 3600
            except ValueError:
                print("时间格式错误，请重新输入。")
                continue
        elif method == '2':
            try:
                hours = float(input("请输入工时（小时）："))
            except ValueError:
                print("输入无效，请输入数字。")
                continue
        else:
            print("无效的选择。")
            continue
        
        hours_dict[name] = hours
        print(f"员工 {name} 的工时为 {hours:.2f} 小时。")
    
    if not hours_dict:
        print("未添加任何员工，该天记录未保存。")
        return
    
    try:
        total_tips = float(input("请输入当天的总小费金额："))
    except ValueError:
        print("输入无效，当天记录未保存。")
        return
    
    daily_records.append({
        'date': date_str,
        'total_tips': total_tips,
        'hours': hours_dict
    })
    print("当天数据保存成功。")

def generate_report():
    # 计算总数据
    total_tips_all = sum(r['total_tips'] for r in daily_records)
    total_hours_all = sum(sum(h.values()) for h in [r['hours'] for r in daily_records])
    avg_tip_per_hour = total_tips_all / total_hours_all if total_hours_all else 0
    
    # 收集所有员工
    all_employees = set()
    for record in daily_records:
        all_employees.update(record['hours'].keys())
    all_employees = sorted(all_employees)
    
    # 计算员工数据
    employee_data = {}
    for emp in all_employees:
        total_hours = 0
        total_tips = 0
        daily_details = []
        
        for record in daily_records:
            hours = record['hours'].get(emp, 0)
            if not hours:
                continue
            
            day_total = sum(record['hours'].values())
            tips = record['total_tips'] * (hours / day_total) if day_total else 0
            
            total_hours += hours
            total_tips += tips
            daily_details.append({
                'date': record['date'],
                'hours': hours,
                'tips': tips
            })
        
        employee_data[emp] = {
            'total_hours': total_hours,
            'total_tips': total_tips,
            'daily_details': daily_details
        }
    
    # 显示报表
    print("\n=== 工资和小费计算报表 ===")
    print(f"总小费：${total_tips_all:.2f}")
    print(f"总工时：{total_hours_all:.2f}小时")
    print(f"平均每小时小费：${avg_tip_per_hour:.2f}\n")
    
    print("=== 员工明细 ===")
    for emp, data in employee_data.items():
        avg = data['total_tips'] / data['total_hours'] if data['total_hours'] else 0
        print(f"\n员工：{emp}")
        print(f"   总工时：{data['total_hours']:.2f}小时")
        print(f"   分得小费：${data['total_tips']:.2f}")
        print(f"   平均每小时小费：${avg:.2f}")
        print("   每日明细：")
        for detail in data['daily_details']:
            print(f"      日期：{detail['date']} - 工时：{detail['hours']:.2f}小时，小费：${detail['tips']:.2f}")
    
    print("\n=== 每日明细 ===")
    for record in daily_records:
        date = record['date']
        tips = record['total_tips']
        hours = record['hours']
        total = sum(hours.values())
        print(f"\n日期：{date}")
        print(f"   总小费：${tips:.2f}")
        print(f"   总工时：{total:.2f}小时")
        print("   员工分配：")
        for emp, h in hours.items():
            if total == 0:
                t = 0
            else:
                t = tips * (h / total)
            print(f"      {emp}: {h:.2f}小时，小费：${t:.2f}")

def main_menu():
    while True:
        print("\n=== 主菜单 ===")
        print("1. 添加员工")
        print("2. 删除员工")
        print("3. 录入每日数据")
        print("4. 生成报表")
        print("5. 退出")
        choice = input("请选择操作：")
        
        if choice == '1':
            add_employee()
        elif choice == '2':
            remove_ployee()
        elif choice == '3':
            input_daily_data()
        elif choice == '4':
            generate_report()
        elif choice == '5':
            print("程序已退出。")
            break
        else:
            print("无效的选项，请重新输入。")

if __name__ == "__main__":
    main_menu()