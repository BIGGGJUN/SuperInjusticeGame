import random
import time
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class HackingSimulator:
    def __init__(self):
        self.player = {
            "name": "",
            "money": 1000,
            "bitcoin": 0,
            "heat": 0,
            "skills": {
                "networking": 1,
                "cryptography": 1,
                "social_engineering": 1,
                "malware": 1,
                "forensics": 1
            },
            "equipment": {
                "computer": {"name": "Basic Laptop", "power": 1},
                "vpn_layers": 0,
                "exploit_kit": [],
                "botnet_size": 0
            },
            "known_exploits": ["buffer_overflow", "sql_injection"],
            "contacts": []
        }
        
        # 세력 시스템
        self.factions = {
            "government": {"name": "정부", "reputation": 0, "alert_level": 1.0},
            "banks": {"name": "금융권", "reputation": 0, "alert_level": 1.0},
            "corps": {"name": "대기업", "reputation": 0, "alert_level": 1.0},
            "criminal": {"name": "범죄조직", "reputation": 0, "alert_level": 0.5},
            "hacktivists": {"name": "핵티비스트", "reputation": 0, "alert_level": 0.3}
        }
        
        self.current_time = datetime.now()
        self.active_processes = []
        self.discovered_systems = []
        self.current_target = None
        self.terminal_history = []
        
        # 상점 아이템
        self.shop_items = {
            "hardware": {
                "Gaming Rig": {"price": 5000, "power": 3, "desc": "고성능 게이밍 컴퓨터"},
                "Server Farm": {"price": 20000, "power": 10, "desc": "서버 팜 구축"},
                "Quantum Computer": {"price": 100000, "power": 50, "desc": "양자 컴퓨터"}
            },
            "software": {
                "VPN Layer": {"price": 500, "desc": "추가 VPN 레이어 (추적 방지)"},
                "Zero-Day Exploit": {"price": 10000, "desc": "제로데이 취약점"},
                "Rootkit": {"price": 3000, "desc": "고급 루트킷"},
                "Cryptolocker": {"price": 5000, "desc": "랜섬웨어 툴킷"}
            },
            "services": {
                "Botnet (100 nodes)": {"price": 2000, "desc": "봇넷 노드 구매"},
                "Inside Contact": {"price": 8000, "desc": "내부 협력자 확보"},
                "Bitcoin Mixer": {"price": 1000, "desc": "비트코인 믹싱 서비스"}
            }
        }
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def slow_print(self, text, delay=0.02):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
        
    def show_prompt(self):
        return f"{self.player['name']}@darkhub:~$ "
        
    def show_status_bar(self):
        print(f"\n┌─[{self.player['name']}]─[${self.player['money']:,}]─[BTC:{self.player['bitcoin']:.2f}]─[Heat:{self.player['heat']}%]─[{self.current_time.strftime('%Y-%m-%d %H:%M')}]")
        print(f"└─[VPN:{self.player['equipment']['vpn_layers']}층]─[Botnet:{self.player['equipment']['botnet_size']}]─[CPU:{self.player['equipment']['computer']['name']}]")
        
    def process_command(self, cmd):
        parts = cmd.strip().split()
        if not parts:
            return
            
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        commands = {
            "help": self.show_help,
            "status": self.show_detailed_status,
            "scan": self.network_scan,
            "contracts": self.show_contracts,
            "hack": self.start_hacking,
            "shop": self.access_shop,
            "factions": self.show_factions,
            "skills": self.show_skills,
            "upgrade": self.upgrade_skill,
            "bitcoin": self.bitcoin_operations,
            "contacts": self.manage_contacts,
            "lay_low": self.lay_low,
            "news": self.show_news,
            "clear": self.clear_screen,
            "exit": self.exit_game
        }
        
        if command in commands:
            commands[command](args)
        else:
            print(f"명령어를 찾을 수 없습니다: {command}")
            print("'help'를 입력하여 사용 가능한 명령어를 확인하세요.")
            
    def show_help(self, args):
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║                    DARKHUB TERMINAL v2.0                      ║
╠══════════════════════════════════════════════════════════════╣
║ 기본 명령어:                                                  ║
║   help              - 도움말 표시                             ║
║   status            - 상세 상태 확인                          ║
║   clear             - 화면 지우기                             ║
║   exit              - 게임 종료                               ║
║                                                               ║
║ 해킹 명령어:                                                  ║
║   scan [network]    - 네트워크 스캔                           ║
║   hack [target]     - 타겟 해킹 시작                          ║
║   contracts         - 의뢰 목록 확인                          ║
║                                                               ║
║ 관리 명령어:                                                  ║
║   shop [category]   - 암시장 접속                             ║
║   factions          - 세력 관계 확인                          ║
║   skills            - 스킬 확인                               ║
║   upgrade [skill]   - 스킬 업그레이드                         ║
║   contacts          - 연락처 관리                             ║
║   bitcoin [action]  - 비트코인 관리                           ║
║   lay_low           - 잠적하기                                ║
║   news              - 최신 뉴스 확인                          ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(help_text)
        
    def show_detailed_status(self, args):
        print("\n" + "="*60)
        print(f"해커명: {self.player['name']}")
        print(f"보유 자금: ${self.player['money']:,}")
        print(f"비트코인: {self.player['bitcoin']:.4f} BTC")
        print(f"추적 레벨: {self.player['heat']}%")
        print(f"\n장비:")
        print(f"  컴퓨터: {self.player['equipment']['computer']['name']} (성능: {self.player['equipment']['computer']['power']})")
        print(f"  VPN 레이어: {self.player['equipment']['vpn_layers']}층")
        print(f"  봇넷 크기: {self.player['equipment']['botnet_size']} nodes")
        print(f"  보유 익스플로잇: {', '.join(self.player['equipment']['exploit_kit']) if self.player['equipment']['exploit_kit'] else '없음'}")
        print("="*60)
        
    def network_scan(self, args):
        if not args:
            networks = ["darknet", "clearnet", "corporate", "government"]
            print("\n사용 가능한 네트워크:")
            for net in networks:
                print(f"  - {net}")
            print("\n사용법: scan [network_name]")
            return
            
        network = args[0].lower()
        print(f"\n{network} 스캔 중...")
        self.slow_print("█" * 20)
        
        targets = self.generate_targets(network)
        
        print(f"\n발견된 시스템 ({len(targets)}개):")
        for i, target in enumerate(targets):
            self.discovered_systems.append(target)
            print(f"  [{i+1}] {target['ip']} - {target['name']} ({target['type']})")
            print(f"      보안 레벨: {'★' * target['security']}")
            print(f"      예상 보상: ${target['reward'][0]:,} - ${target['reward'][1]:,}")
            
    def generate_targets(self, network):
        targets = []
        
        if network == "darknet":
            target_types = [
                {"name": "Underground Market", "type": "market", "security": 2, "reward": (2000, 5000)},
                {"name": "Hacker Forum", "type": "forum", "security": 1, "reward": (1000, 3000)},
                {"name": "Crypto Exchange", "type": "crypto", "security": 3, "reward": (5000, 15000)}
            ]
        elif network == "corporate":
            target_types = [
                {"name": "TechCorp Database", "type": "database", "security": 3, "reward": (3000, 8000)},
                {"name": "MegaCorp Email Server", "type": "email", "security": 2, "reward": (2000, 5000)},
                {"name": "StartUp Cloud", "type": "cloud", "security": 2, "reward": (1500, 4000)}
            ]
        elif network == "government":
            target_types = [
                {"name": "City Records", "type": "records", "security": 3, "reward": (4000, 10000)},
                {"name": "Federal Database", "type": "federal", "security": 5, "reward": (10000, 30000)},
                {"name": "Military Network", "type": "military", "security": 6, "reward": (15000, 50000)}
            ]
        else:
            target_types = [
                {"name": "Personal Blog", "type": "personal", "security": 1, "reward": (500, 1500)},
                {"name": "Small Business", "type": "business", "security": 2, "reward": (1000, 3000)}
            ]
            
        for t in target_types:
            target = t.copy()
            target["ip"] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            target["faction"] = self.get_faction_for_target(t["type"])
            targets.append(target)
            
        return targets
        
    def get_faction_for_target(self, target_type):
        faction_map = {
            "federal": "government",
            "military": "government",
            "records": "government",
            "database": "corps",
            "email": "corps",
            "cloud": "corps",
            "crypto": "banks",
            "market": "criminal",
            "forum": "hacktivists"
        }
        return faction_map.get(target_type, None)
        
    def start_hacking(self, args):
        if not args:
            if not self.discovered_systems:
                print("\n먼저 'scan'으로 타겟을 찾으세요.")
                return
                
            print("\n발견된 타겟:")
            for i, target in enumerate(self.discovered_systems[-5:]):
                print(f"  {target['ip']} - {target['name']}")
            print("\n사용법: hack [target_ip]")
            return
            
        target_ip = args[0]
        target = None
        
        for system in self.discovered_systems:
            if system['ip'] == target_ip:
                target = system
                break
                
        if not target:
            print(f"\n타겟을 찾을 수 없습니다: {target_ip}")
            return
            
        self.current_target = target
        self.run_hacking_session(target)
        
    def run_hacking_session(self, target):
        print(f"\n╔══════════════════════════════════════════════════════════════╗")
        print(f"║ 타겟: {target['name']:<45} ║")
        print(f"║ IP: {target['ip']:<47} ║")
        print(f"║ 보안 레벨: {'★' * target['security']:<42} ║")
        print(f"╚══════════════════════════════════════════════════════════════╝")
        
        # 해킹 단계
        stages = [
            {"name": "정찰", "commands": ["nmap", "whois", "dig"], "required": 1},
            {"name": "스캐닝", "commands": ["port_scan", "vuln_scan", "service_enum"], "required": 2},
            {"name": "접근", "commands": ["exploit", "bruteforce", "social_engineer"], "required": 1},
            {"name": "권한 상승", "commands": ["privesc", "rootkit", "backdoor"], "required": 1},
            {"name": "데이터 추출", "commands": ["download", "exfiltrate", "encrypt"], "required": 1}
        ]
        
        current_stage = 0
        stage_progress = defaultdict(int)
        success = True
        detection_level = 0
        
        print("\n해킹 세션 시작...")
        print("'help_hack'으로 사용 가능한 명령어를 확인하세요.")
        
        while current_stage < len(stages):
            stage = stages[current_stage]
            prompt = f"\n[{stage['name']}] {self.player['name']}@{target['ip']}:~$ "
            cmd = input(prompt).strip().lower()
            
            if cmd == "help_hack":
                print(f"\n현재 단계: {stage['name']}")
                print(f"사용 가능한 명령어: {', '.join(stage['commands'])}")
                print(f"필요한 성공 횟수: {stage['required']}")
                continue
                
            if cmd == "abort":
                print("\n해킹을 중단합니다...")
                self.player['heat'] += 5
                return
                
            if cmd in stage['commands']:
                self.slow_print(f"\n{cmd} 실행 중...")
                
                # 성공 확률 계산
                skill_bonus = self.calculate_skill_bonus(cmd)
                equipment_bonus = self.player['equipment']['computer']['power'] * 5
                vpn_bonus = self.player['equipment']['vpn_layers'] * 3
                
                base_chance = 80 - (target['security'] * 10)
                total_chance = base_chance + skill_bonus + equipment_bonus
                
                if random.randint(1, 100) <= total_chance:
                    self.slow_print(f"[SUCCESS] {cmd} 성공!")
                    stage_progress[current_stage] += 1
                    
                    if stage_progress[current_stage] >= stage['required']:
                        print(f"\n[단계 완료] {stage['name']} 완료!")
                        current_stage += 1
                else:
                    self.slow_print(f"[FAILED] {cmd} 실패!")
                    detection_level += random.randint(5, 15)
                    
                # 탐지 체크
                detection_level += random.randint(1, 5) - vpn_bonus
                if detection_level >= 100:
                    print("\n[경고] 침입이 탐지되었습니다!")
                    self.handle_detection(target)
                    return
                    
                print(f"탐지 레벨: {detection_level}%")
            else:
                print("잘못된 명령어입니다.")
                
        # 해킹 성공
        self.handle_success(target)
        
    def calculate_skill_bonus(self, command):
        skill_map = {
            "nmap": "networking",
            "port_scan": "networking",
            "vuln_scan": "networking",
            "exploit": "malware",
            "bruteforce": "cryptography",
            "social_engineer": "social_engineering",
            "privesc": "malware",
            "rootkit": "malware",
            "encrypt": "cryptography",
            "exfiltrate": "forensics"
        }
        
        skill = skill_map.get(command, "networking")
        return self.player['skills'][skill] * 5
        
    def handle_success(self, target):
        reward = random.randint(*target['reward'])
        bitcoin_reward = reward / 50000  # 비트코인 변환
        
        print(f"\n╔══════════════════════════════════════════════════════════════╗")
        print(f"║                      해킹 성공!                               ║")
        print(f"╚══════════════════════════════════════════════════════════════╝")
        
        # 보상 선택
        print(f"\n획득 가능한 보상:")
        print(f"1. 현금: ${reward:,}")
        print(f"2. 비트코인: {bitcoin_reward:.4f} BTC")
        print(f"3. 데이터 판매 (세력 평판 영향)")
        
        choice = input("\n선택: ")
        
        if choice == "1":
            self.player['money'] += reward
            print(f"\n${reward:,} 획득!")
        elif choice == "2":
            self.player['bitcoin'] += bitcoin_reward
            print(f"\n{bitcoin_reward:.4f} BTC 획득!")
        elif choice == "3":
            self.sell_data_to_faction(target, reward)
            
        # 세력 영향
        if target['faction']:
            self.factions[target['faction']]['reputation'] -= 10
            self.factions[target['faction']]['alert_level'] *= 1.2
            print(f"\n{self.factions[target['faction']]['name']} 평판 -10")
            
        # 스킬 향상
        improved_skill = random.choice(list(self.player['skills'].keys()))
        self.player['skills'][improved_skill] += 1
        print(f"{improved_skill} 스킬 +1")
        
        # Heat 증가
        heat_gain = target['security'] * 5
        self.player['heat'] = min(100, self.player['heat'] + heat_gain)
        
    def sell_data_to_faction(self, target, base_reward):
        print("\n데이터를 판매할 세력:")
        factions = ["government", "corps", "criminal", "hacktivists"]
        for i, faction in enumerate(factions, 1):
            if faction != target['faction']:
                print(f"{i}. {self.factions[faction]['name']} (평판: {self.factions[faction]['reputation']})")
                
        choice = input("\n선택: ")
        if choice.isdigit() and 1 <= int(choice) <= len(factions):
            buyer = factions[int(choice) - 1]
            
            # 평판에 따른 보너스
            rep_bonus = 1 + (self.factions[buyer]['reputation'] / 100)
            final_reward = int(base_reward * rep_bonus * 1.2)
            
            self.player['money'] += final_reward
            self.factions[buyer]['reputation'] += 15
            
            print(f"\n{self.factions[buyer]['name']}에 데이터 판매!")
            print(f"보상: ${final_reward:,} (평판 보너스 포함)")
            print(f"{self.factions[buyer]['name']} 평판 +15")
            
    def handle_detection(self, target):
        print("\n[경보] 보안팀이 대응 중입니다!")
        
        # 세력별 대응 속도
        if target['faction']:
            alert_level = self.factions[target['faction']]['alert_level']
            response_time = int(60 / alert_level)  # 초 단위
            
            print(f"예상 도착 시간: {response_time}초")
            print("빠르게 흔적을 지우고 탈출하세요!")
            
            # 탈출 미니게임
            commands_needed = ["clean_logs", "kill_process", "vpn_hop", "disconnect"]
            for cmd in commands_needed:
                user_cmd = input(f"\n긴급: {cmd}를 입력하세요! > ")
                if user_cmd == cmd:
                    self.slow_print(f"{cmd} 실행됨!")
                else:
                    print("실패! 추적 레벨 증가!")
                    self.player['heat'] += 10
                    
        self.player['heat'] = min(100, self.player['heat'] + target['security'] * 10)
        
    def show_contracts(self, args):
        contracts = self.generate_contracts()
        
        print("\n╔══════════════════════════════════════════════════════════════╗")
        print("║                        의뢰 목록                              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        
        for i, contract in enumerate(contracts, 1):
            print(f"\n[{i}] {contract['title']}")
            print(f"    의뢰자: {contract['client']}")
            print(f"    타겟: {contract['target']}")
            print(f"    보상: ${contract['reward']:,}")
            print(f"    난이도: {'★' * contract['difficulty']}")
            print(f"    설명: {contract['description']}")
            
        print("\n의뢰를 수락하려면 'hack [target_ip]'를 사용하세요.")
        
    def generate_contracts(self):
        contracts = []
        
        # 세력별 의뢰 생성
        for faction_id, faction in self.factions.items():
            if faction['reputation'] > -50:  # 평판이 너무 낮으면 의뢰 없음
                if faction_id == "government" and faction['reputation'] > 20:
                    contracts.append({
                        "title": "국가 안보 위협 제거",
                        "client": "정부 기관",
                        "target": "175.23.45.67",
                        "reward": 15000 + (faction['reputation'] * 100),
                        "difficulty": 4,
                        "description": "테러리스트 서버 무력화"
                    })
                elif faction_id == "corps" and faction['reputation'] > 10:
                    contracts.append({
                        "title": "산업 스파이 활동",
                        "client": "대기업",
                        "target": "203.15.78.90",
                        "reward": 8000 + (faction['reputation'] * 50),
                        "difficulty": 3,
                        "description": "경쟁사 신제품 정보 탈취"
                    })
                elif faction_id == "criminal" and faction['reputation'] > 0:
                    contracts.append({
                        "title": "금융 정보 탈취",
                        "client": "익명",
                        "target": "88.45.123.200",
                        "reward": 10000 + (faction['reputation'] * 80),
                        "difficulty": 3,
                        "description": "은행 고객 데이터베이스 접근"
                    })
                    
        # 개인 의뢰
        personal_contracts = [
            {
                "title": "불륜 증거 수집",
                "client": "개인 의뢰자",
                "target": "192.168.1.100",
                "reward": 3000,
                "difficulty": 1,
                "description": "배우자의 이메일과 메시지 확인"
            },
            {
                "title": "복수 해킹",
                "client": "익명 개인",
                "target": "10.0.0.50",
                "reward": 5000,
                "difficulty": 2,
                "description": "전 직장 상사의 컴퓨터 마비"
            }
        ]
        
        contracts.extend(random.sample(personal_contracts, min(2, len(personal_contracts))))
        return contracts
        
    def show_factions(self, args):
        print("\n╔══════════════════════════════════════════════════════════════╗")
        print("║                        세력 관계                              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        
        for faction_id, faction in self.factions.items():
            rep = faction['reputation']
            status = "적대적" if rep < -30 else "비우호적" if rep < 0 else "중립" if rep < 20 else "우호적" if rep < 50 else "동맹"
            
            print(f"\n{faction['name']}:")
            print(f"  평판: {rep} ({status})")
            print(f"  경계 레벨: {faction['alert_level']:.1f}x")
            
            # 평판에 따른 효과
            if rep >= 50:
                print("  보너스: 의뢰 보상 +50%, 경찰 대응 -30%")
            elif rep >= 20:
                print("  보너스: 의뢰 보상 +20%")
            elif rep <= -30:
                print("  페널티: 즉시 추적, 의뢰 없음")
                
    def access_shop(self, args):
        if not args:
            print("\n암시장 카테고리:")
            print("  - hardware (하드웨어)")
            print("  - software (소프트웨어)")
            print("  - services (서비스)")
            print("\n사용법: shop [category]")
            return
            
        category = args[0].lower()
        if category not in self.shop_items:
            print("잘못된 카테고리입니다.")
            return
            
        print(f"\n╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    암시장 - {category.upper():<25} ║")
        print(f"╚══════════════════════════════════════════════════════════════╝")
        print(f"보유 자금: ${self.player['money']:,}")
        
        items = self.shop_items[category]
        for name, item in items.items():
            print(f"\n{name}:")
            print(f"  가격: ${item['price']:,}")
            print(f"  설명: {item['desc']}")
            
        print("\n구매하려면: shop buy [item_name]")
        
        if len(args) > 1 and args[0] == "buy":
            item_name = " ".join(args[1:])
            self.buy_item(category, item_name)
            
    def buy_item(self, category, item_name):
        # 아이템 찾기
        for cat, items in self.shop_items.items():
            for name, item in items.items():
                if name.lower() == item_name.lower():
                    if self.player['money'] >= item['price']:
                        self.player['money'] -= item['price']
                        
                        # 아이템 효과 적용
                        if "Computer" in name:
                            self.player['equipment']['computer'] = {"name": name, "power": item['power']}
                        elif name == "VPN Layer":
                            self.player['equipment']['vpn_layers'] += 1
                        elif name == "Botnet":
                            self.player['equipment']['botnet_size'] += 100
                        elif name in ["Zero-Day Exploit", "Rootkit", "Cryptolocker"]:
                            self.player['equipment']['exploit_kit'].append(name)
                            
                        print(f"\n{name} 구매 완료!")
                        return
                    else:
                        print("\n자금이 부족합니다!")
                        return
                        
        print("아이템을 찾을 수 없습니다.")
        
    def bitcoin_operations(self, args):
        if not args:
            print("\n비트코인 작업:")
            print(f"  현재 보유: {self.player['bitcoin']:.4f} BTC")
            print("  - bitcoin mine (채굴)")
            print("  - bitcoin sell [amount] (판매)")
            print("  - bitcoin mix (믹싱 - Heat 감소)")
            return
            
        action = args[0]
        
        if action == "mine":
            power = self.player['equipment']['computer']['power']
            botnet = self.player['equipment']['botnet_size']
            
            mining_power = power + (botnet / 100)
            mined = random.uniform(0.0001, 0.001) * mining_power
            
            print(f"\n채굴 중...")
            self.slow_print("█" * 10)
            
            self.player['bitcoin'] += mined
            print(f"\n{mined:.6f} BTC 채굴 완료!")
            
        elif action == "sell" and len(args) > 1:
            try:
                amount = float(args[1])
                if amount <= self.player['bitcoin']:
                    price = random.randint(40000, 60000)  # BTC 가격
                    profit = int(amount * price)
                    
                    self.player['bitcoin'] -= amount
                    self.player['money'] += profit
                    
                    print(f"\n{amount:.4f} BTC를 ${profit:,}에 판매했습니다.")
                else:
                    print("보유한 비트코인이 부족합니다.")
            except ValueError:
                print("올바른 금액을 입력하세요.")
                
        elif action == "mix":
            if self.player['bitcoin'] >= 0.01:
                self.player['bitcoin'] -= 0.01
                heat_reduction = random.randint(10, 25)
                self.player['heat'] = max(0, self.player['heat'] - heat_reduction)
                
                print(f"\n비트코인 믹싱 완료!")
                print(f"추적 레벨 -{heat_reduction}%")
            else:
                print("최소 0.01 BTC가 필요합니다.")
                
    def lay_low(self, args):
        print("\n잠적 중...")
        locations = ["안전가옥", "해외 서버팜", "다크넷 카페", "VPN 체인"]
        location = random.choice(locations)
        
        self.slow_print(f"{location}에서 대기 중...")
        time.sleep(2)
        
        # VPN 보너스
        vpn_bonus = self.player['equipment']['vpn_layers'] * 5
        heat_reduction = random.randint(15, 30) + vpn_bonus
        
        self.player['heat'] = max(0, self.player['heat'] - heat_reduction)
        
        # 시간 경과
        self.current_time += timedelta(hours=random.randint(6, 24))
        
        print(f"\n추적 레벨 -{heat_reduction}%")
        
        # 랜덤 이벤트
        if random.random() < 0.3:
            self.random_event()
            
    def random_event(self):
        events = [
            {
                "text": "다크넷에서 새로운 제로데이 취약점 정보를 발견했습니다!",
                "effect": lambda: self.player['equipment']['exploit_kit'].append("New Zero-Day")
            },
            {
                "text": "해커 동료가 연락처를 공유했습니다.",
                "effect": lambda: self.player['contacts'].append(f"Hacker_{random.randint(1000, 9999)}")
            },
            {
                "text": "암호화폐 가격이 급등했습니다!",
                "effect": lambda: setattr(self.player, 'bitcoin', self.player['bitcoin'] * 1.5)
            }
        ]
        
        event = random.choice(events)
        print(f"\n[이벤트] {event['text']}")
        event['effect']()
        
    def show_news(self, args):
        print("\n╔══════════════════════════════════════════════════════════════╗")
        print("║                      DARKNET NEWS                             ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        
        news = [
            f"정부 사이버 보안 예산 {random.randint(10, 50)}% 증가",
            f"새로운 랜섬웨어 '{random.choice(['DarkLock', 'CryptoReaper', 'ShadowCrypt'])}' 등장",
            f"다크넷 마켓 '{random.choice(['SilkRoad3', 'AlphaBay2', 'DarkMarket'])}' 폐쇄",
            f"비트코인 가격 ${random.randint(30000, 70000)}",
            f"FBI, 해커 {random.randint(5, 20)}명 체포"
        ]
        
        for i, item in enumerate(random.sample(news, 3), 1):
            print(f"\n[{i}] {item}")
            
    def show_skills(self, args):
        print("\n╔══════════════════════════════════════════════════════════════╗")
        print("║                         스킬                                  ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        
        for skill, level in self.player['skills'].items():
            print(f"\n{skill.replace('_', ' ').title()}:")
            print(f"  레벨: {level}")
            print(f"  진행도: {'█' * level}{'░' * (10 - min(level, 10))}")
            print(f"  업그레이드 비용: ${level * 2000}")
            
    def upgrade_skill(self, args):
        if not args:
            print("\n스킬을 지정하세요. 예: upgrade networking")
            return
            
        skill = args[0].lower()
        if skill in self.player['skills']:
            cost = self.player['skills'][skill] * 2000
            
            if self.player['money'] >= cost:
                self.player['money'] -= cost
                self.player['skills'][skill] += 1
                print(f"\n{skill} 스킬이 레벨 {self.player['skills'][skill]}로 상승했습니다!")
            else:
                print(f"\n자금이 부족합니다. 필요: ${cost:,}")
        else:
            print("존재하지 않는 스킬입니다.")
            
    def manage_contacts(self, args):
        if not self.player['contacts']:
            print("\n연락처가 없습니다.")
            return
            
        print("\n╔══════════════════════════════════════════════════════════════╗")
        print("║                        연락처                                 ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        
        for contact in self.player['contacts']:
            print(f"  - {contact}")
            
        print("\n연락처는 특별한 의뢰나 정보를 제공할 수 있습니다.")
        
    def check_game_over(self):
        if self.player['heat'] >= 100:
            self.clear_screen()
            print("\n" + "="*60)
            print("                    GAME OVER")
            print("="*60)
            print("\n당신은 추적당해 체포되었습니다.")
            print(f"\n최종 통계:")
            print(f"  보유 자금: ${self.player['money']:,}")
            print(f"  비트코인: {self.player['bitcoin']:.4f} BTC")
            print(f"  완료한 해킹: {len(self.discovered_systems)}")
            
            # 최고 평판 세력
            best_faction = max(self.factions.items(), key=lambda x: x[1]['reputation'])
            print(f"  최고 우호 세력: {best_faction[1]['name']} ({best_faction[1]['reputation']})")
            
            return True
        return False
        
    def exit_game(self, args):
        print("\n시스템을 종료합니다...")
        self.slow_print("로그 삭제 중...")
        exit()
        
    def start_game(self):
        self.clear_screen()
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║         ___   ___   ___   _  __  _   _  _   _  ___          ║
║        |   \\ | _ | | _ \\ | |/ / | | | || | | || _ )         ║
║        | |) || _ | |   / | ' <  | |_| || |_| || _ \\         ║
║        |___/ |___| |_|_\\ |_|\\_\\ |_____||_____||___/         ║
║                                                              ║
║                    HACKING SIMULATOR v2.0                    ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        self.slow_print("\n시스템 초기화 중...")
        time.sleep(1)
        
        self.player['name'] = input("\n해커 핸들을 입력하세요: ")
        
        print(f"\n환영합니다, {self.player['name']}.")
        print("\n당신은 이제 다크넷의 일원입니다.")
        print("정부, 기업, 범죄조직 사이에서 균형을 유지하며")
        print("최고의 해커가 되어야 합니다.")
        
        print("\n시작 장비:")
        print("  - Basic Laptop")
        print("  - $1,000")
        print("  - 기본 익스플로잇 킷")
        
        print("\n'help'를 입력하여 명령어를 확인하세요.")
        
        input("\n계속하려면 Enter...")
        self.clear_screen()
        
        # 메인 게임 루프
        while True:
            if self.check_game_over():
                break
                
            self.show_status_bar()
            cmd = input(self.show_prompt())
            self.terminal_history.append(cmd)
            self.process_command(cmd)
            
            # 시간 경과
            self.current_time += timedelta(minutes=random.randint(5, 30))

# 게임 실행
if __name__ == "__main__":
    game = HackingSimulator()
    game.start_game()