

class PatternUtil() :

    def pattern_names(self):
        self.pattern_names = {
            1: '제품구성',
            2: '서비스일반',
            3: '배송일반',
            4: '제품불만',
            5: '구매문의',
            6: '서비스변경',
            7: '가격문의',
            8: '결제문의',
            9: '배송변경',
            10: '배송지연',
            11: '배송현황',
            12: '환불문의',
            13: '제품문의',
            14: '결제변경',
            15: '서비스신청',
            16: '서비스취소',
            17: '매장문의',
            18: '서비스정지',
            19: '영수증문의',
            20: '해줘요',
            21 : '뭔가요',
            22 : '있나요',
            23 : '오나요',
            24 : '하냐',
            25: '왔어요',
            26 : '건가요',
            27 : '되냐',
            28 : '알려줘',
            29 : '야',
            30 : '나요',
            31 : '없나요',
            32 : '달라',
            33 : '했어요',
            34 : '어요',
            35 : '됬',
            36 : '부서졌어요',
            37 : '냐',
            38 : '할래',
            39 : '싶어',
            40 : '같아요',
            41 : '싸다,비싸다',
            42 : '스러운가',
            43 : '안',
            44 : '좋아',
            45 : '봐',
            46 : '갔었어',
            47 : '~예요',
            48 : '모든패턴',
            49 : '줘',
            50: '니',
            51 : '중',
            52 : '겟네',
            53 : '싫어',
            54 : '알',
            55: '텐데',
            56: '괜찮을까',
            57: '먹고'
        }


    def __init__(self, mecab):

        self.patterns = {}
        self.mecab = mecab

        ## 제품 구성
        self.product_composition_patterns = [('있', 'VV'), ('뭔', 'MM'), ('무엇', 'NP'), ('뭐', 'NP')
            , ('뭐', 'IC'), ('오', 'VV'), ('하', 'XSV'), ('인가요', 'VCP+EF'),('해', 'XSV+EC'),('해줘요', 'XSV+EC+VX+EC'),
                                        ('되', 'VV'), ('건가요', 'NNB+VCP+EF'), ('건가요', 'NNB+VCP+EC'), ('뭔가요', 'NP+VCP+EF'),
                                        ('알려줘', 'VV+EC+VX+EC'), ('와', 'VV+EF'), ('와', 'VV+EC'), ('야', 'VCP+EF'), ('야', 'VCP+EC'),
                                             ('나요', 'EF'),('나요', 'EC'), ('한가요', 'XSA+EF'), ('한가요', 'XSA+EC')
                                             ]
        self.patterns[1] = self.product_composition_patterns

        ## 서비스 일반문의
        self.service_patterns = [('있', 'VA'), ('오', 'VV'), ('한가요', 'XSA+EF'), ('한가', 'XSA+EC'), ('나요', 'EF'), ('나요', 'EC'),
                            ('있', 'VA'),
                            ('뭔', 'MM'), ('무엇', 'NP'), ('뭐', 'NP'), ('뭐', 'IC'), ('되', 'VV'), ('하', 'XSA'),
                            ('하', 'XSV'), ('건가요', 'NNB+VCP+EC'),
                            ('건가요', 'NNB+VCP+EF'), ('건가', 'NNB+VCP+EC'), ('건가', 'NNB+VCP+EF'), ('인가요', 'VCP+EF'),
                            ('인가요', 'VCP+EC'), ('인가', 'VCP+EC')
                            ,('인가', 'VCP+EF'), ('뭔가요', 'NP+VCP+EF'), ('뭔가', 'NP+VCP+EF'), ('뭔가', 'NP+VCP+EC')
                            ]
        self.patterns[2] = self.service_patterns


        ## 배송 일반 문의
        self.delivery_patterns = [('있', 'VV'), ('있', 'VA'), ('되', 'XSV'), ('되', 'VV'), ('하', 'XSA'), ('하', 'XSV'), ('인가요', 'VCP+EC'),
                             ('인가요', 'VCP+EF'),
                             ('인가', 'VCP+EF'), ('오', 'VV')]
        self.patterns[3] = self.delivery_patterns


        ## 제품불만
        self.complaint_patterns = [('없', 'VA'), ('네요', 'VCP+EC'), ('네요', 'VCP+EF'), ('달라요', 'VA+EF'), ('달라요', 'VA+EC'),
                              ('했', 'XSV+EP'), ('어요', 'EF'), ('어요', 'EC'),('됬', 'VV+EP'),
                              ('했어요', 'XSV+EP+EC'), ('왔', 'VV+EP'), ('왔어요', 'VV+EP+EC'), ('부서졌', 'VV+EP'), ('있', 'VA'),
                              ('있', 'VV')]
        self.patterns[4] = self.complaint_patterns

        ## 구매문의
        self.buy_patterns = [('있', 'VV'), ('있', 'VA'), ('한가요', 'XSA+EF'), ('한가요', 'XSA+EC'), ('한가', 'XSA+EC'),
                        ('한가', 'XSA+EF'), ('해', 'XSA+EF'), ('해', 'XSA+EC'), ('냐', 'EF'), ('냐', 'EC')]
        self.patterns[5] = self.buy_patterns


        ## 서비스 변경 문의
        self.service_change_patterns = [
            ('하', 'VV'), ('하나', 'NR'), ('한가요', 'XSA+EF'), ('한가요', 'XSA+EC'), ('해', 'XSA+EF'), ('해', 'XSA+EC'),
            ('한가', 'XSA+EF'), ('한가', 'XSA+EC')
        ]
        self.patterns[6] = self.service_change_patterns

        ## 가격 문의
        self.price_patterns = [
            ('되', 'VV'), ('건가요', 'NNB+VCP+EF'), ('있', 'VV'), ('하', 'XSV'), ('같', 'VA'), ('비싸', 'VA'), ('비싸', 'VA+EF'),
            ('비싸', 'VA+EC'), ('싸', 'VA')
            , ('싸', 'VV+EC'), ('싸', 'VV+EF'), ('아요', 'EC'), ('아요', 'EF')
        ]
        self.patterns[7] = self.price_patterns

        ## 결제 문의
        self.payment_patterns = [
            ('하', 'VV'), ('하나', 'NR'), ('한가요', 'XSA+EF'), ('한가요', 'XSA+EC'), ('해', 'XSA+EF'), ('해', 'XSA+EC'),
            ('하', 'XSA'), ('같', 'VA')
        ]
        self.patterns[8] = self.payment_patterns

        ## 배송 변경 문의
        self.delivery_change_patterns = [('있', 'VV'), ('나요', 'EF'), ('나요', 'EC')]
        self.patterns[9] = self.delivery_change_patterns

        ## 배송 딜레이 문의
        self.delivery_delay_patterns = [('안', 'MAG')]
        self.patterns[10] = self.delivery_delay_patterns


        ## 배송 현황
        self.delivery_list_patterns = [('있', 'VV')]
        self.patterns[11] = self.delivery_list_patterns


        ## 환불 문의
        self.refund_patterns = [('한가요', 'XSA+EF'), ('한가요', 'XSA+EC'), ('한가', 'XSA+EC'), ('한가', 'XSA+EF'),
                           ('싶', 'VX'), ('할래', 'VV+EF'), ('할래', 'VV+EC'), ('되', 'VV')]
        self.patterns[12] = self.refund_patterns


        ## 제품문의
        self.product_patterns = [('없', 'VA'), ('스러운가', 'XSA+EF'), ('스러운가', 'XSA+EC'), ('스럽', 'XSA'), ('다른가', 'VA+EF'),
                            ('다른가', 'VA+EC')]
        self.patterns[13] = self.product_patterns


        ## 결제변경
        self.payment_change_patterns = [
            ('싶', 'VX'), ('할', 'XSV+ETM'), ('해', 'XSA+EF'), ('해', 'XSA+EC')
        ]
        self.patterns[14] = self.payment_change_patterns


        ## 서비스 신청
        self.service_app_patterns = [
            ('하', 'VV'), ('해', 'VV+EF'), ('해', 'VV+EC'), ('하나', 'NR')
        ]
        self.patterns[15] = self.service_app_patterns

        ## 서비스 취소
        self.service_cancel_patterns = [
            ('하', 'VV'), ('하', 'VX'), ('해', 'VV+EF'), ('해', 'VV+EC')
        ]
        self.patterns[16] = self.service_cancel_patterns

        ## 매장문의
        self.shap_patterns = [
            ('있', 'VV'), ('인가요', 'VCP+EF'), ('인가요', 'VCP+EC'), ('인가', 'VCP+EF'), ('인가', 'VCP+EC'), ('이', 'VCP'),
            ('임', 'VCP+ETN'), ('있', 'VA')
        ]
        self.patterns[17] = self.shap_patterns

        ## 서비스 정지 문의
        self.service_stop_patterns = [
            ('있', 'VA')
        ]
        self.patterns[18] = self.service_stop_patterns

        ### 영수증 문의
        self.receipt_patterns = [
            ('한가요', 'XSA+EF'), ('한가요', 'XSA+EC'), ('한가', 'XSA+EF'), ('한가', 'XSA+EC'), ('하', 'XSA'), ('하나', 'NR')
        ]
        self.patterns[19] = self.receipt_patterns

        ### 해줘요
        self.doing_patterns = [
            ('해', 'XSV+EC'), ('해줘요', 'XSV+EC+VX+EC'), ('해줘요', 'XSV+EC+VX+EF'), ('해요', 'XSV+EC'), ('해요', 'XSV+EF'),
            ('해','VV+EC'), ('해야함', 'VV+EC+VX+ETN'), ('해야', 'VV+EC')
        ]
        self.patterns[20] = self.doing_patterns

        ### 뭔가요
        self.what_patterns = [
            ('뭔', 'MM'), ('무엇', 'NP'), ('뭐', 'NP'), ('뭐', 'IC'), ('뭔가', 'NP+VCP+EF'), ('뭔가', 'NP+VCP+EC'), ('뭔가요', 'NP+VCP+EF')
        ]
        self.patterns[21] = self.what_patterns

        ### 있나요+인가요?
        self.be_patterns = [
            ('있', 'VV'), ('있', 'VA'), ('인가요', 'VCP+EF'), ('인가', 'VCP+EF'), ('인가', 'VCP+EC'),  ('인가요', 'VCP+EC'), ('인', 'VCP+ETM')
        ]
        self.patterns[22] = self.be_patterns

        ### 오나요?
        self.come_patterns = [
            ('오', 'VV'), ('왔', 'VV+EP'), ('와', 'VV+EF'), ('와', 'VV+EC'), ('와', 'JKB')
        ]
        self.patterns[23] = self.come_patterns

        ### 하냐?
        self.let_patterns = [
            ('하', 'XSV'), ('하', 'VV'), ('한가요', 'XSA+EF'), ('한가요', 'XSA+EC'), ('한가', 'XSA+EC')
        ]
        self.patterns[24] = self.let_patterns

        ### 왔어요
        self.arrival_patterns = [
            ('왔', 'VV+EP'), ('왔어요', 'VV+EP+EC'), ('다녀왔', 'VV+EP'), ('갔다왔', 'VV+EP')
        ]
        self.patterns[25] = self.arrival_patterns

        ### 건가요
        self.why_patterns = [
            ('건가요', 'NNB+VCP+EC'), ('건가요', 'NNB+VCP+EF'), ('건가', 'NNB+VCP+EC'), ('건가', 'NNB+VCP+EF'), ('건가', 'NNB+VCP+EC+VCP')
        ]
        self.patterns[26] = self.why_patterns

        ### 되냐
        self.can_patterns = [
            ('되', 'VV'), ('되', 'XSV'), ('될까', 'XSV+EF'), ('될까', 'XSV+EC'), ('돼', 'VV+EF'), ('돼요', 'VV+EF'), ('돼', 'VV+EC'),
            ('돼요', 'VV+EC'), ('된다', 'VV+EC'), ('된다', 'VV+EF'), ('됨', 'VV+ETN')
        ]
        self.patterns[27] = self.can_patterns

        ### 알려줘
        self.know_patterns = [
            ('알려줘', 'VV+EC+VX+EC'),('알려', 'VV+EC'), ('알', 'VV+ETM')
        ]
        self.patterns[28] = self.know_patterns

        ### ~야?
        self.normal_patterns = [
            ('야', 'VCP+EF'), ('야', 'VCP+EC'), ('야', 'EF'), ('야', 'EC')
        ]
        self.patterns[29] = self.normal_patterns

        ### ~나요?
        self.nayo_patterns = [
            ('나요', 'EF'), ('나요', 'EC'), ('나요', 'VCP+EF')
        ]
        self.patterns[30] = self.nayo_patterns

        ### ~없나요?
        self.no_patterns = [
            ('없', 'VA')
        ]
        self.patterns[31] = self.no_patterns

        ### ~달라?
        self.different_patterns = [
            ('달라요', 'VA+EF'), ('달라요', 'VA+EC'), ('다르', 'VA'), ('달라', 'VA+EC')
        ]
        self.patterns[32] = self.different_patterns

        ### 했어요
        self.done_patterns = [
            ('했', 'XSV+EP'), ('했어요', 'XSV+EP+EC'), ('했어요', 'XSV+EP+EF'),  ('함', 'XSV+ETN'), ('해', 'XSV+EC')
        ]
        self.patterns[33] = self.done_patterns

        ### 어요
        self.ayo_patterns = [
            ('어요', 'EF'), ('어요', 'EC')
        ]
        self.patterns[34] = self.ayo_patterns

        ### 됬어요
        self.be_patterns = [
            ('됬', 'VV+EP')
        ]
        self.patterns[35] = self.be_patterns

        #### 부서졌어요
        self.broke_patterns = [
            ('부서졌', 'VV+EP')
        ]
        self.patterns[36] = self.broke_patterns

        #### 냐
        self.yaa_patterns = [
            ('냐', 'EF'), ('냐', 'EC')
        ]
        self.patterns[37] = self.yaa_patterns

        #### 할래
        self.shall_patterns = [
            ('할래', 'VV+EF'), ('할래', 'VV+EC'), ('할래', 'XSV+EF'), ('할래', 'XSV+EC')
        ]
        self.patterns[38] = self.shall_patterns

        self.want_patterns = [
            ('싶', 'VX'), ('싶', 'VV')
        ]
        self.patterns[39] = self.want_patterns

        self.same_patterns = [
            ('같', 'VA')
        ]
        self.patterns[40] = self.same_patterns

        self.cheap_patterns = [
            ('비싸', 'VA+EC'), ('싸', 'VA'), ('비싸', 'VA'), ('비싸', 'VA+EF'), ('싸', 'VV+EC'), ('싸', 'VV+EF')
        ]
        self.patterns[41] = self.cheap_patterns

        self.snop_patterns = [
            ('스러운가', 'XSA+EF'), ('스러운가', 'XSA+EC'), ('스럽', 'XSA'), ('스러워', 'XSA+EC'), ('스러워', 'XSA+EF'), ('스러운', 'XSA+ETM')
        ]
        self.patterns[42] = self.snop_patterns


        self.not_patterns = [
            ('안', 'MAG')
        ]

        self.patterns[43] = self.not_patterns

        self.like_patterns = [
            ('좋', 'VA'),  ('좋아해', 'VV+EC'),  ('좋아해', 'VV+EF')
        ]

        self.patterns[44] = self.like_patterns

        self.see_patterns = [
            ('봐', 'VV+EC'), ('봐', 'VV+EF'), ('봐', 'VX+EC'), ('봐', 'VX+EF')
        ]
        self.patterns[45] = self.see_patterns

        self.gone_patterns = [
            ('갔었', 'VV+EP'), ('갔', 'VV+EP'),  ('갓', 'VA')
        ]
        self.patterns[46] = self.gone_patterns

        self.yyo_patterns = [
            ('에요', 'EF'), ('에요', 'EC'), ('예요', 'EF'), ('예요', 'EC'), ('예', 'NNG'), ('예요', 'VCP+EF'), ('요', 'JX')
        ]
        self.patterns[47] = self.yyo_patterns

        self.patterns[48] = []

        self.patterns[49] = [('줘', 'VX+EC'), ('줘', 'VX+EF')]

        self.patterns[50] = [('니', 'EF'), ('니', 'EC')]

        self.patterns[51] = [('중임', 'NNG'),('중', 'NNB')]

        self.patterns[52] = [('겠', 'EP')]

        self.patterns[53] = [('싫', 'VA'), ('시러', 'XSA+EC'), ('시러', 'XSA+EF')]


        self.patterns[54] = [('알', 'VV'), ('아니', 'IC'), ('아니', 'VCN')]


        self.patterns[55] = [('텐데', 'NNB+VCP+EC')]

        self.patterns[56] = [('괜찮', 'VA')]

        self.patterns[57] = [('먹', 'VV')]



    def check_response_pattern(self, intent_pattern, poss):

        is_position = False
        for pos in poss:
            if pos in intent_pattern:
                is_position = True
                break
        return is_position


    def check_intent_rule(self, question):
        results = []
        poss = self.mecab.pos(question)

        # print("poss ====>", poss)
        for index, pattern in self.patterns.items() :
            if index == 48 :
                is_pattern = True
            else :
                is_pattern = self.check_response_pattern(pattern, poss)
            if is_pattern :
                results.append(index)
        return results