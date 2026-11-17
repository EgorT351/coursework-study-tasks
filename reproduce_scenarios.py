from pathlib import Path
import json, tempfile, subprocess, shutil, sys
root=Path(__file__).resolve().parent
e=root/'evidence'
cases=[
('01','Пустой список','2\n0\n','Сохранённых заданий нет.',None),
('02','Добавление','1\nЛР 3\nКачество ИС\n2\n0\n','1. ЛР 3 | Качество ИС | Не выполнено',None),
('03','Пустое название','1\n \nКачество ИС\n0\n','Название задания не может быть пустым.',None),
('04','Неверное меню','9\n0\n','Некорректный пункт меню.',None),
('05','Выполнение','1\nЛР 3\nКачество ИС\n3\n1\n2\n0\n','1. ЛР 3 | Качество ИС | Выполнено',None),
('06','Нет номера','3\n99\n4\n99\n0\n','Задание с таким номером не найдено.',None),
('07','Удаление','1\nЛР 3\nКачество ИС\n4\n1\n2\n0\n','Сохранённых заданий нет.',None),
('08','Нечисловой номер','3\nabc\n0\n','Ошибка ввода:',None),
('09','Повреждение JSON','','Ошибка чтения файла:','corrupt'),
('10','Отказ записи','1\nЛР 3\nКачество ИС\n0\n','Ошибка записи файла:','write')]
(e/'test_plan.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2))
results=[]
for num,name,inputs,expected,setup in cases:
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp)
  for f in ['main.py','task_manager.py']: shutil.copy(root/f,p/f)
  if setup=='corrupt': (p/'tasks.json').write_text('{')
  if setup=='write': (p/'tasks.json.tmp').mkdir()
  run=subprocess.run([sys.executable,str(p/'main.py')],input=inputs,text=True,capture_output=True)
  out=run.stdout+run.stderr
  (e/f'case_{num}.txt').write_text(out)
  results.append(dict(id=num,name=name,input=inputs,expected=expected,actual=next((line for line in out.splitlines() if expected in line),out[-200:]),passed=expected in out and run.returncode==0))
(e/'test_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)
 for f in ['main.py','task_manager.py']: shutil.copy(root/f,p/f)
 runs=[]
 for inputs in ['1\nЛР 3 — тестирование\nКачество и надежность ИС\n1\nКурсовая работа\nКачество и надежность ИС\n2\n3\n1\n2\n0\n','2\n0\n']:
  r=subprocess.run([sys.executable,str(p/'main.py')],input=inputs,text=True,capture_output=True)
  runs.append(r.stdout)
 for i,out in enumerate(runs,1): (e/f'demo_{i}.txt').write_text(out)
 data=json.loads((p/'tasks.json').read_text())
 assert len(data)==2 and data[0]['status']=='Выполнено'
 (e/'demo_tasks.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print([(r['id'],r['passed']) for r in results])
assert all(r['passed'] for r in results)
