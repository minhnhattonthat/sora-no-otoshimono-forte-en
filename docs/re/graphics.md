# Graphics with Japanese text: inventory

Source: `work/gfx/<folder>/<name>.png` (601 images, 21 folders), checked sheet by sheet and opened at 2-3x where the thumbnail was too small.
English follows `glossary.md` where it has the term. "Garbled" means the dump has tiles in the wrong order or no palette (grey). It needs a proper render before the text can be read or edited.

## Summary

Images with Japanese text, by folder (garbled ones that clearly or almost certainly contain JP are counted):

| folder | JP images | of total | notes |
|---|---|---|---|
| ActionChoice | 3 | 3 | menu header, cards, buttons |
| AdvTalk | 5 | 5 | ADV window parts, Yes/No, system messages |
| AutoSave | 2 | 2 | load/save error screens |
| Book | 2 | 2 | Member Roster (sound test) screen; Book_Interface garbled |
| DelusionSelect | 73 | 96 | 66 = Training_UpBG0/1/2_00-21 stat panels; 44 unique scenario blurbs |
| Demo | 26 | 26 | 24 character profile panels (8 chars x 3 pages) + return-to-title prompt |
| EmblemList | 3 | 3 | Title List screen |
| EventSub | 16 | 18 | all garbled; tutorial screenshots |
| Friendly | 2 | 2 | Intimacy screen header + Back button |
| Help | 25 | 27 | all garbled: 19 help-text pages, 4 windows, 2 list/common sheets |
| Logo | 1 | 4 | Kadokawa Shoten logo only (corporate logo, probably leave) |
| MainTitle | 4 | 15 | title logo, main menu buttons (2 colour states), copyright |
| NormalSub | 0 | 1 | |
| Option | 3 | 4 | 2 options pages; UpBG garbled (logo) |
| Result | 24 | 26 | 22 identical "Communication Over!" banners + 2 results panels |
| ShowTitle | 7 | 15 | 6 episode title cards + logo |
| StaffRoll | 227 | 241 | 7 identical credit sets x 32 strips + All Clear + 2 logos |
| TomokiMonitor | 70 | 70 | all garbled (grey, no palette); 60 title-name strips |
| TomokiTraining | 5 | 15 | training UI + 10 hint banners; 10 up-screen images garbled |
| Trial_TrialInterface | 4 | 6 | Happening Time logo, Success/Failure, Game Over, Pause |
| Wallpaper | 4-5 | 20 | **looks like leftover Strike Witches assets**, mostly garbled |
| **Total** | **~506** | **601** | far fewer distinct texts: see repeats below |

Same text repeated across many files:
- **StaffRoll**: `StaffRoll_Down00..06_00-32` are 7 colour/character variants with identical credit text and layout, so the 32 credit strips need translating once and redrawing 7 times (224 files). `_32` is blank in every set.
- **Result_UpBG00-21**: 22 banners all reading コミュニケーション終了！ over different art. Five of them (07, 10, 14, 15, 20) have the text set vertically for the rotated-DS layout.
- **DelusionSelect Training_UpBG0/1/2_00-21**: all 66 share the same 5 stat labels (煩悩耐久力 etc. + LV). UpBG1/UpBG2 (44) also share the "Situation No. / Communication Type / Replay or Advanced Delusion / Fastest Finish / Best Clear Rank" panel. Only the 3-line blurb at the bottom differs, with one unique blurb per UpBG1/UpBG2 file. UpBG0 (22) has the stat labels only.
- **Demo_InfoBG**: 8 characters x 3 pages (stats / bio / quote). Each text is unique.
- **TomokiMonitor emblem strips**: Monitor_Emblem00-19, Monitor_Load_Emblem00-19 and Monitor_Save_Emblem00-19 look like the same 20 title names in 3 styles (Load_ and Save_ look pixel-identical).
- **Stat labels** (煩悩耐久力/指先技術力/変態紳士力/生存本能力/異性懐柔力) also appear in TomokiTraining_DownTEX00 and Trial_Various_Pause.
- **はい/いいえ/OK buttons**: AdvTalk_02_m, EmblemList_TEX01, Training_DownTEX01, Trial_Various_Pause.
- **モドル (Back) button**: AdvTalk_01_m, DelusionSelect Training_DownMisc01, EmblemList_TEX00, Friendly_TEX00, Option_Tex01, Training_DownTEX00, Book_Interface.
- **Game logo** (そらのおとしもの フォルテ / ドリーミーシーズン): MainTitle Title_Second_TEX00, ShowTitle_Logo_TEX, StaffFin_Up, StaffRoll_Up, StaffRoll_DownNN_00 (as text), Option_UpBG (OBJ cells; renders fine with the NCER, small copy at scale ~0.395, 166,117). Same art everywhere: TEX00 rect 0 (224x136) is the logo, 'Dreamy Season' sits at logo + (95,120); StaffRoll_Up/StaffFin_Up have it baked at 19,17 (StaffFin_Up = StaffRoll_Up through an affine RGB tint). At boot the logo quad is revealed left to right in the glow palette Title_Second_TEX00_ef.NCLR (= normal colours x2), then fades to the normal palette and 'Dreamy Season' (rect 1, rect 2 = its white flash copy) fades in. English logo: gfx/edits/MainTitle/logo_en.py (lettering after Funimation's "Heaven's Lost Property Forte" logo over the game's own wing swoosh; katakana reading dropped).
- **Main menu buttons**: Title_Second_TEX01 (blue) and TEX02 (pink selected state) have the same 8 labels.
- **Tutorial chalkboard** DelusionSelect/Event_00_50_s and its garbled copy EventSub/Event_00_50.

---

## ActionChoice

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| ActionChoice | ActionChoice_BG | screen header | 行動選択 | Action Select | header tab over pattern bg |
| ActionChoice | ActionChoice_TEX | mode cards + buttons | 妄想コミュニケーション / 智樹☆トレーニング / イベント選択 (card captions and pill buttons); メニュー (small button) | Delusion Communication / Tomoki☆Training / Event Select; Menu | each label twice (tiny card caption + big pill); "NEXT" card already English |
| ActionChoice | ActionChoice_TEXPlus | extra mode cards + buttons | 称号リスト / 親密度 / ？？？ | Title List / Intimacy / ??? | captions + pills, as above |

## AdvTalk

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| AdvTalk | AdvTalk_00_m | ADV window parts (blue) | ×ボタン | X Button | tiny label with icon; rest is frames |
| AdvTalk | AdvTalk_10_m | ADV window parts (pink) | ×ボタン | X Button | pink copy of _00 |
| AdvTalk | AdvTalk_01_m | ADV system buttons | スキップ (x3, animated logo), モドル, オート (x3) | Skip, Back, Auto | SAVE/LOAD/OPTION/TITLE/BACK LOG already English |
| AdvTalk | AdvTalk_02_m | return-to-title dialog | タイトルに戻ります; はい / いいえ (3 colour sets) | Return to title?; Yes / No | MENU, HELP already English |
| AdvTalk | Interface_00_m | system message text | バックアップメモリの初期化中です / トモ☆コレが追加されました。 | Initializing backup memory... / Tomo☆Colle added. | plain white text on transparent bg |

## AutoSave

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| AutoSave | LoadError | error screen | データを読めませんでした。電源を切って、カードを差込み直してください | Could not read data. Turn the power off and reinsert the Game Card. | white text on black |
| AutoSave | SaveError | error screen | データを書けませんでした。電源を切って、カードを差込み直してください | Could not write data. Turn the power off and reinsert the Game Card. | white text on black |

## Book

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| Book | Book_BG | Member Roster (sound/voice viewer) | 部員名簿; 名前 / 表情 / セリフ / BGM / 背景; ▶セリフ再生Ⓐ ▶BGM再生Ⓧ ■BGM停止Ⓨ; ◀-10Ⓛ Ⓡ+10▶ | Member Roster; Name / Expression / Line / BGM / Background; Play line, Play BGM, Stop BGM; -10 / +10 | text over notebook panel |
| Book | Book_Interface | sprite strip | モドル (+ button icons) | Back | 256x16 strip, partly garbled, needs proper render |

## DelusionSelect

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| DelusionSelect | Event_00_25_m | tutorial chalkboard | おしえて イカロス先生 / DS本体を持ち替えて下さい / ニンフ (tiny) | Teach Me, Ikaros-sensei / Please turn your DS sideways | text over chalkboard art with chibi Ikaros/Nymph |
| DelusionSelect | Event_00_50_s | tutorial chalkboard | コミュニケーションモードの操作説明！ / X・Bまたは十字ボタンの上下で 画面スクロール / 下画面をタッチすると タッチ操作 / 下画面をなぞると スライド操作 | Communication Mode controls! / X/B or +Control Pad up/down: scroll screen / Touch the Touch Screen: touch action / Trace the Touch Screen: slide action | chalk text over chalkboard; garbled copy in EventSub/Event_00_50 |
| DelusionSelect | FreeTraining_DownBG | screen header | フリーコミュニケーション | Free Communication | header tab |
| DelusionSelect | Training_DownBG | screen header | 妄想コミュニケーション | Delusion Communication | header tab |
| DelusionSelect | Training_DownMisc00 | character name plates | イカロス / ニンフ / アストレア / 見月 そはら / 五月田根 美香子 / 守形 英四郎 / トモ子 | Ikaros / Nymph / Astraea / Sohara Mitsuki / Mikako Satsukitane / Eishiro Sugata / Tomoko | plates next to eye-strip portraits |
| DelusionSelect | Training_DownMisc01 | buttons/labels | ⓧ智樹☆トレーニングへ (x2); モドル; リプレイ妄想 (x4 styles); アドバンス妄想 (x5 styles); コミュニケーションタイプ | To Tomoki☆Training; Back; Replay Delusion; Advanced Delusion; Communication Type | NEW badges already English |
| DelusionSelect | Training_UpCommon | sprite sheet | fragments of リプレイ妄想 / アドバンス妄想 + digits | Replay / Advanced Delusion | garbled - needs proper render |
| DelusionSelect | Training_UpBG0_00 - _21 (22 files) | stat panel over character art | 煩悩耐久力 LV / 指先技術力 LV / 変態紳士力 LV / 生存本能力 LV / 異性懐柔力 LV | Lust Endurance / Finger Technique / Pervert Gentleman / Survival Instinct / Charm (LV) | same 5 labels in all 22; text over art |
| DelusionSelect | Training_UpBG1_00 - _21, Training_UpBG2_00 - _21 (44 files) | scenario info panel | stat labels as UpBG0 + シチュエーションNo. / コミュニケーションタイプ / リプレイ妄想 (UpBG1) or アドバンス妄想 (UpBG2) / 最速フィニッシュ / 最高クリアランク + unique 3-line blurb (below) | Situation No. / Communication Type / Replay Delusion or Advanced Delusion / Fastest Finish / Best Clear Rank | shared panel text; blurbs listed one per file below |
| DelusionSelect | Training_UpBG1_00 | blurb | そはらやニンフの服が智樹にお手入れされるのを見たイカロスは、自分の服にもお手入れをお願いした。 | After seeing Tomoki "tend to" Sohara's and Nymph's clothes, Ikaros asked him to tend to hers too. | |
| DelusionSelect | Training_UpBG1_01 | blurb | 智樹は、シールを探すため、イカロスに身体を調べさせてくれとストレートに頼むのであった。 | To find the sticker, Tomoki bluntly asks Ikaros to let him examine her body. | |
| DelusionSelect | Training_UpBG1_02 | blurb | ニンフのように自分もマッサージしてほしいとお願いするイカロス。彼女に対して智樹は……。 | Ikaros asks for a massage like Nymph got. And Tomoki's response is... | |
| DelusionSelect | Training_UpBG1_03 | blurb | 分身のイカロスからのお願いで、智樹はイカロスの身体を調べることになった。 | At the request of Ikaros's double, Tomoki ends up examining Ikaros's body. | |
| DelusionSelect | Training_UpBG1_04 | blurb | ニンフは自分の力で服が飛ぶのを抑えていたのだが、結局は智樹のお手入れを受け入れるのだった。 | Nymph had been using her power to keep her clothes from flying off, but in the end she accepts Tomoki's tending. | |
| DelusionSelect | Training_UpBG1_05 | blurb | 虫がついている、などといって身体に貼られたシールを探そうとする智樹を、ニンフは疑いつつも受け入れる。 | Claiming she has a bug on her, Tomoki tries to hunt for the sticker on her body; Nymph is suspicious but goes along. | |
| DelusionSelect | Training_UpBG1_06 | blurb | 興奮すると爆発する首輪をつけられてしまった智樹。ニンフの挑発に乗った智樹の運命は……？ | Tomoki is stuck wearing a collar that explodes if he gets excited. He takes Nymph's bait; what fate awaits him...? | |
| DelusionSelect | Training_UpBG1_07 | blurb | アストレア同様2人に増えたニンフ。智樹は多少強引にでもニンフが本物かどうかを確かめるのであった。 | Like Astraea, Nymph has doubled. Tomoki checks, a little forcefully, whether this Nymph is the real one. | |
| DelusionSelect | Training_UpBG1_08 | blurb | カードの力で、智樹のことを先生だと思い込んでいるアストレアを保健室に連れ込んだ智樹は……。 | A Card has Astraea convinced Tomoki is her teacher, and he takes her into the nurse's office... | |
| DelusionSelect | Training_UpBG1_09 | blurb | 妄想で煩悩を発散させることに味をしめた智樹は、次に女教師となったアストレアの妄想をするのであった。 | Hooked on venting his lust through delusions, Tomoki next imagines Astraea as a female teacher. | |
| DelusionSelect | Training_UpBG1_10 | blurb | カードのせいで2人に増えたアストレア。智樹はどちらが本物か当てることができるのか……！ | A Card has doubled Astraea. Can Tomoki guess which one is real...!? | |
| DelusionSelect | Training_UpBG1_11 | blurb | 去年の写真を見て文化祭に興味を持ったアストレア。智樹はアストレアがコスプレ喫茶で働く様を妄想する……。 | Last year's photos get Astraea interested in the school festival. Tomoki imagines her working at a cosplay café... | |
| DelusionSelect | Training_UpBG1_12 | blurb | カードの力で服が飛んでいく騒動を治めるため、智樹はそはらのチア衣装のお手入れを行うことになった。 | To end the Card-caused clothes-flying chaos, Tomoki has to tend to Sohara's cheerleader outfit. | |
| DelusionSelect | Training_UpBG1_13 | blurb | 爆発首輪を装着した智樹なら、Hなことはされないと考えたそはらは智樹に水泳を教えてもらうのだが……。 | Figuring Tomoki can't try anything naughty while wearing the exploding collar, Sohara has him teach her to swim, but... | |
| DelusionSelect | Training_UpBG1_14 | blurb | 守形のアドバイスにより、妄想で煩悩を発散させることにした智樹は、そはらの妄想で発散させるのであった。 | On Sugata's advice to vent his lust through delusions, Tomoki vents it with a Sohara delusion. | |
| DelusionSelect | Training_UpBG1_15 | blurb | カードの力で智樹を教師と誤認識している美香子に対して、智樹は英語の発音指導をするのだった。 | A Card has Mikako mistaking Tomoki for a teacher, so he coaches her English pronunciation. | |
| DelusionSelect | Training_UpBG1_16 | blurb | さらなる過激な妄想を求める智樹は、美香子のライブ衣装の妄想を行うことにしたのであった。 | Seeking ever more extreme delusions, Tomoki decides to imagine Mikako in a concert outfit. | |
| DelusionSelect | Training_UpBG1_17 | blurb | 散歩中、夏祭りの準備をしている美香子と出会った智樹は、会長の浴衣姿を妄想するのであった……。 | On a walk, Tomoki runs into Mikako preparing for the summer festival and imagines the President in a yukata... | |
| DelusionSelect | Training_UpBG1_18 | blurb | 智樹は、皆の身体のどこかに貼られたシールを探すため、守形の均整のとれた肉体をまさぐる破目になった。 | Hunting for the stickers stuck somewhere on everyone's bodies, Tomoki ends up groping Sugata's well-proportioned physique. | |
| DelusionSelect | Training_UpBG1_19 | blurb | 量子変換機でトモ子になった智樹は変身っぷりを確かめるために自らの身体をチェックするのだった。 | Turned into Tomoko by the Quantum Converter, Tomoki checks his own body to see how complete the change is. | |
| DelusionSelect | Training_UpBG1_20 | blurb | 守形の量子変換機でトモ子になった智樹は、ちゃんと自分が女の子になれているかどうか、確かめてみるのだった。 | Turned into Tomoko by Sugata's Quantum Converter, Tomoki checks whether he has really become a girl. | |
| DelusionSelect | Training_UpBG1_21 | blurb | 興奮すると爆発する事件の最中。智樹はトモ子化した自分に対してなら興奮しなくなると思ったのだが……。 | Mid explode-when-excited incident, Tomoki thought he'd stay calm around his own Tomoko self, but... | |
| DelusionSelect | Training_UpBG2_00 | blurb | イカロスとお医者さんごっこに興じることになったのだが、はたしてイカロスの反応は……？ | Tomoki ends up playing doctor with Ikaros; how will she react...? | |
| DelusionSelect | Training_UpBG2_01 | blurb | 母イカロスにテストの点数で叱られるダメ息子智樹は、母に孝行するためにマッサージをしようとするのだが……。 | Scolded over his test scores by Mother Ikaros, no-good son Tomoki tries a massage to make it up to her, but... | |
| DelusionSelect | Training_UpBG2_02 | blurb | スク水メイド、イカロス。智樹はちょっと天然な彼女に、メイドとしての心得を教え込むのだった。 | Swimsuit maid Ikaros. Tomoki drills his slightly airheaded maid in proper maid conduct. | |
| DelusionSelect | Training_UpBG2_03 | blurb | 転校生イカロスと街角で衝突！智樹は転んだ彼女を気遣ってやさしく介抱するのであった。 | Tomoki collides with transfer student Ikaros on a street corner! He gently looks after her when she falls. | |
| DelusionSelect | Training_UpBG2_04 | blurb | 貴族令嬢ニンフとその従者智樹。智樹は舞踏会帰りのニンフの命令でドレスの手入れを行うのだった。 | Noble lady Nymph and her servant Tomoki. Back from the ball, she orders him to tend to her dress. | |
| DelusionSelect | Training_UpBG2_05 | blurb | ニンフに足踏みマッサージされたい智樹。辛抱たまらずニンフにお願いをするのだが……。 | Tomoki wants Nymph to give him a foot-stomping massage. Unable to resist, he asks her, but... | |
| DelusionSelect | Training_UpBG2_06 | blurb | 小鳥が好きなニンフのために、智樹は自らが量子変換機で小鳥になって慰めることにしたのだが……。 | For bird-loving Nymph, Tomoki uses the Quantum Converter to turn himself into a little bird to comfort her, but... | |
| DelusionSelect | Training_UpBG2_07 | blurb | ニンフと智樹が姉弟に！？素直じゃないけど小さくてかわいい姉に対して智樹は……。 | Nymph and Tomoki as siblings!? Faced with a big sister who's prickly but small and cute, Tomoki... | |
| DelusionSelect | Training_UpBG2_08 | blurb | 智樹とアストレアが兄妹に！？破天荒な妹に翻弄される智樹のとある日々の1コマ。 | Tomoki and Astraea as siblings!? A day in Tomoki's life, at the mercy of his wild little sister. | |
| DelusionSelect | Training_UpBG2_09 | blurb | 新人OLアストレアと先輩社員智樹。後輩の度を超えたドジっぷりにキレた智樹のとった行動とは！？ | Rookie office lady Astraea and senior employee Tomoki. Her extreme clumsiness makes him snap, and what does he do!? | |
| DelusionSelect | Training_UpBG2_10 | blurb | カメラマン智樹が街でスカウトしてきた謎の少女アストレア。彼女を被写体にして撮影は進行していくのだが……。 | Photographer Tomoki scouts a mysterious girl, Astraea, on the street. The photo shoot with her as the model goes on, but... | |
| DelusionSelect | Training_UpBG2_11 | blurb | アストレアバニーをはべらせる智樹。そそうをした彼女を智樹は……。 | Tomoki with bunny-girl Astraea at his side. When she slips up, Tomoki... | 2 lines only |
| DelusionSelect | Training_UpBG2_12 | blurb | チア部の合宿に同行する鬼コーチ智樹。皆が寝静まったころに、そはらへ秘密の特訓を行うのだった……。 | Demon coach Tomoki joins the cheer club's training camp. Once everyone's asleep, he gives Sohara secret special training... | |
| DelusionSelect | Training_UpBG2_13 | blurb | 海でイルカとたわむれるそはら。だが、そのイルカは量子変換機で変身した智樹だった！ | Sohara frolics with a dolphin at sea. But the dolphin is Tomoki, transformed by the Quantum Converter! | |
| DelusionSelect | Training_UpBG2_14 | blurb | 何故か先輩後輩の関係になった智樹とそはら。勉強会の後にマッサージをすることになったのだが……。 | Somehow Tomoki and Sohara are senior and junior. After a study session, a massage is in order, but... | |
| DelusionSelect | Training_UpBG2_15 | blurb | 女スパイ美香子を捕まえた智樹。彼女の身体から機密情報の入ったマイクロフィルムは見つけられるか！？ | Tomoki captures female spy Mikako. Can he find the microfilm with the secret intel on her body!? | |
| DelusionSelect | Training_UpBG2_16 | blurb | ロックスター美香子と付き人智樹。智樹はツアーで疲れた美香子にマッサージをするのだが……。 | Rock star Mikako and her assistant Tomoki. He massages the tour-weary Mikako, but... | |
| DelusionSelect | Training_UpBG2_17 | blurb | お風呂上りの美香子の色っぽい姿を妄想する智樹。やはり彼女には和装が似合うと痛感するのであった。 | Tomoki imagines a sultry, fresh-from-the-bath Mikako, and is reminded that traditional dress really suits her. | |
| DelusionSelect | Training_UpBG2_18 | blurb | 過酷な修行を続けてきたトモ子の最後のターゲットは守形。果たして彼を超えることはできるのか！？ | After grueling training, Tomoko's final target is Sugata. Can she surpass him!? | |
| DelusionSelect | Training_UpBG2_19 | blurb | ボクサーを目指して訓練に励む中、縄飛びの縄が絡みついてしまうトモ子。なんとか抜け出そうとするのだが……。 | Training to become a boxer, Tomoko gets tangled in her jump rope. She tries to wriggle free, but... | |
| DelusionSelect | Training_UpBG2_20 | blurb | 智樹とトモ子が分裂してしまった！煩悩（智樹）が分離したキレイなトモ子は、どのような反応を見せるのか。 | Tomoki and Tomoko have split apart! How will the "pure" Tomoko, freed of her lust (Tomoki), react? | |
| DelusionSelect | Training_UpBG2_21 | blurb | アイドルを目指すトモ子はネコミミ姿でエクササイズをはじめるのだった。 | Aspiring idol Tomoko starts exercising in cat ears. | |

No text: Training_DownThumb00 - Training_DownThumb22 (23 portrait strips).

## Demo

Character profile panels: `_00` = name/stats, `_01` = bio, `_02` = quote. Text is in a light-blue box beside the character art.

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| Demo | Demo_InfoBG00_00 | profile: stats | イカロス（戦略エンジェロイド タイプα） CV/早見沙織 162cm 48kg B.W.H(88・57・85) 趣味：なでなで 座右の銘：マスター。 | Ikaros (Strategic Angeloid Type α), CV: Saori Hayami. Hobby: head pats. Motto: "Master." | |
| Demo | Demo_InfoBG00_01 | profile: bio | ゲームのヒロイン。空から降ってきた未確認生物。白い天使のような翼を持つ少女の姿をしている。極度の世間知らず。自らを「愛玩用エンジェロイド」と名乗り、智樹の願いを叶えるため、不思議なカードを使う。 | The game's heroine. An unidentified creature who fell from the sky, shaped like a girl with white angel wings. Extremely naive. Calls herself a "Pet-class Angeloid" and uses mysterious Cards to grant Tomoki's wishes. | 10 lines |
| Demo | Demo_InfoBG00_02 | profile: quote | 「でも……もしかしたら、この最後のカードが叶えたのは、私の願いなのかも……。」 | "But... maybe what this last Card granted was my wish..." | pink text |
| Demo | Demo_InfoBG01_00 | profile: stats | ニンフ（電子戦用エンジェロイド タイプβ） CV/野水伊織 139cm 29kg B.W.H(72・45・68) 趣味：おやつ 座右の銘：なにそれ…わかんない…。 | Nymph (Electronic Warfare Angeloid Type β), CV: Iori Nomizu. Hobby: snacks. Motto: "What's that... I don't get it..." | |
| Demo | Demo_InfoBG01_01 | profile: bio | イカロスに続いて、空からやってきた第二の未確認生物。七色に光る透明な羽を持っている。ちょっとわがままな性格で、ツンデレの気あり。お菓子が大好き。 | The second unidentified creature from the sky, after Ikaros. Has clear wings that shine in seven colours. A bit selfish, with tsundere tendencies. Loves sweets. | |
| Demo | Demo_InfoBG01_02 | profile: quote | 「トモキと2人っきりで、いい感じの雰囲気になれたらいいなぁ……なんて。」 | "It'd be nice to be alone with Tomoki and have things get kinda romantic... just kidding." | |
| Demo | Demo_InfoBG02_00 | profile: stats | アストレア（局地戦用エンジェロイド タイプΔ） CV/福原香織 159cm 48kg B.W.H(91・56・86) 趣味：ハイッ！！趣味ってなんですか！！こたつは大好きです！！ 座右の銘：まんぷく！！ | Astraea (Close-Combat Angeloid Type Δ), CV: Kaori Fukuhara. Hobby: "Yes!! What's a hobby!? I love kotatsu!!" Motto: "Full belly!!" | |
| Demo | Demo_InfoBG02_01 | profile: bio | 智樹抹殺の命を受け、地上に降りてきた第三の未確認生物。その戦闘能力はイカロスをも上回るが、電算能力が弱いため、ちょっとおバカ。 | The third unidentified creature, sent to Earth with orders to eliminate Tomoki. Her combat ability even beats Ikaros's, but her computing power is weak, so she's a bit dim. | |
| Demo | Demo_InfoBG02_02 | profile: quote | 「あ……そうだ、今度アンタにバカを教えてあげようか？それなら、なんかできそうだし！」 | "Oh... I know, how about I teach YOU to be dumb next time? I think I could manage that!" | |
| Demo | Demo_InfoBG03_00 | profile: stats | 見月そはら（みつき そはら） CV/美名 158cm そんなの聞いちゃだめ！！ B.W.H(92・59・84) 趣味：料理（下手だけど） 裁縫（ものすごいものができるけど） 花を育てること（死滅するけど） 座右の銘：希望 | Sohara Mitsuki, CV: Mina. "Don't ask that!!" Hobbies: cooking (badly), sewing (makes amazing things... sort of), growing flowers (they all die). Motto: Hope. | |
| Demo | Demo_InfoBG03_01 | profile: bio | 智樹の隣家に住む幼なじみ。元気で明るい性格。一人暮らしの智樹のことをなにかと気にかけている。突然、智樹の家に住み着いたイカロスのことが気になる様子。 | Tomoki's childhood friend and next-door neighbour. Cheerful and energetic. Always looks out for Tomoki, who lives alone. Seems bothered by Ikaros suddenly moving into his house. | |
| Demo | Demo_InfoBG03_02 | profile: quote | 「で、でも……！これが私の願い事で私の気持ちなんだから……」 | "B-but...! This is my wish, and how I feel..." | |
| Demo | Demo_InfoBG04_00 | profile: stats | 五月田根美香子（さつきたね みかこ） CV/高垣彩陽 164cm 46kg B.W.H(83・54・80) 趣味：人をオモチャにすること 座右の銘：支配、混沌、破壊。 | Mikako Satsukitane, CV: Ayahi Takagaki. Hobby: toying with people. Motto: Domination, chaos, destruction. | |
| Demo | Demo_InfoBG04_01 | profile: bio | 智樹の通う学校の生徒会長。空美町いちばんのセレブ。守形とは幼なじみ。美人で物腰は柔らかいが、腹黒い性格。 | Student Council President at Tomoki's school, and the richest girl in Sorami Town. Sugata's childhood friend. Beautiful and soft-spoken, but scheming. | |
| Demo | Demo_InfoBG04_02 | profile: quote | 「ああ……桜井くんの悲鳴って会長、とっても好きだわ～。癒されるわね～～～。」 | "Ahh... the President just loves Sakurai-kun's screams~. So soothing~~~." | |
| Demo | Demo_InfoBG05_00 | profile: stats | 守形英四郎（すがた えいしろう） CV/鈴木達央 172cm 58kg 趣味：新大陸捜索 座右の銘：だがそれは「現実」の理論にすぎん。 | Eishiro Sugata, CV: Tatsuhisa Suzuki. Hobby: searching for the New World. Motto: "But that is merely the logic of 'reality'." | |
| Demo | Demo_InfoBG05_01 | profile: bio | 智樹たちの通う学校にある「新大陸発見部」のただ一人の部員。手作りの飛行機で飛ぶことと、空に浮かぶ「新大陸」の発見に情熱をかけており、学校内では変わり者として有名。 | Sole member of the New World Discovery Club at Tomoki's school. Passionate about flying his homemade plane and finding the "New World" floating in the sky; known around school as an oddball. | |
| Demo | Demo_InfoBG05_02 | profile: quote | 「いつか俺が新大陸への扉を開くとき、隣にいる助手がお前なのを嬉しく思うぞ……。」 | "Someday, when I open the door to the New World, I'll be glad the assistant at my side is you..." | |
| Demo | Demo_InfoBG06_00 | profile: stats | トモ子（量子変換器がもたらした中二の夢） CV/藤田咲 きゃるる～～ん♡トモ子でぇ～～す！ | Tomoko (a chuunibyou dream brought by the Quantum Converter), CV: Saki Fujita. "Kyururu~n♡ It's Tomoko~!" | |
| Demo | Demo_InfoBG06_01 | profile: bio | 乙女のヒ・ミ・ツは、そう簡単に教えないぞっ！ | A maiden's se-cre-ts aren't that easy to get, you know! | 2 lines |
| Demo | Demo_InfoBG06_02 | profile: quote | 「女の子同士だから好きなだけ触れちゃうしー、女湯も女子更衣室もOKだしー。」 | "We're both girls, so I can touch all I want~, and the girls' bath and locker room are fair game~." | |
| Demo | Demo_InfoBG07_00 | profile: stats | 桜井智樹（さくらい ともき） CV/保志総一朗 150cm 49kg 趣味：漫画、小説のエロシーン探し 座右の銘：果報は寝て待て | Tomoki Sakurai, CV: Soichiro Hoshi. Hobbies: manga, hunting for erotic scenes in novels. Motto: Good things come to those who wait (sleeping). | |
| Demo | Demo_InfoBG07_01 | profile: bio | ゲームの主人公。「平和が一番」をモットーにする普通の中学生だったが、イカロスと出会い、その日常は破壊されていくことに。生来のスケベ心から、とんでもない妄想が現実のものに……！？ | The game's protagonist. An ordinary middle schooler whose motto was "Peace above all," until meeting Ikaros wrecked his everyday life. Thanks to his born lechery, outrageous delusions come true...!? | |
| Demo | Demo_InfoBG07_02 | profile: quote | 「はぁ……俺は平和な毎日とエロいことさえあれば幸せなのに……。」 | "Sigh... all I need to be happy is peaceful days and naughty stuff..." | |
| Demo | Demo_InputBG | return-to-title prompt | 何かボタンを押す または 下画面をタッチ すると タイトルに戻ります。 | Press any button or touch the Touch Screen to return to the title. | text over pink bg with chibi art |
| Demo | Demo_InputOBJ | sprite version of the prompt | 何かボタンを押す / 下画面をタッチ (fragments) | (same as above) | garbled - needs proper render |

## EmblemList

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| EmblemList | EmblemList_BG | Title List screen | 称号リスト; 達成率 % | Title List; Completion % | header + small box |
| EmblemList | EmblemList_TEX00 | buttons/sprites | モドル | Back | digits, 1/4-4/4, L/R, NEW already English |
| EmblemList | EmblemList_TEX01 | dialog parts | この称号をセットしますか？; 解放条件; はい x3 / いいえ x3 | Set this title?; Unlock condition; Yes / No | OK buttons already English |

## EventSub

All 18 are garbled (tiles out of order) and need a proper render.

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| EventSub | Event_00_50 | tutorial chalkboard | Communication Mode controls text (fragments: 操作説明！, 画面スクロール, タッチ操作, なぞる, スライド操作) | same as DelusionSelect/Event_00_50_s | garbled; likely a duplicate of Event_00_50_s |
| EventSub | Event_00_51 - Event_00_65 (15 files) | tutorial screenshots of Communication Mode | UI labels (fragments: フィーリング, コミュニケーション) + dialogue-box lines (fragments: トモちゃん……, 目が……怖いよ……, ふざけて……) | (unreadable until rendered) | garbled; JP clearly visible in 53, 55, 58, 59, 60, 63, 64, 65; the rest probably have it too |

No text (as far as visible): Event_00_00, Event_03_05 (starfield, garbled).
Rendered properly (OBJ cells): text only in 50, 53, 55, 57-60, 63, 64 (all have specs); 51, 52, 54, 56, 61, 62 have none,
65 is "GAME OVER" (already English).

## EventMain (Communication tutorial screenshots, bottom screen)

Each Event_00_NN is two 128x256 NCBR halves (`NN0` = screen rows 0-127, `NN1` = 128-255) stored turned 90 deg: specs
use `"rotate": 90`. Most are event CGs (no text). Text in:

| file | Japanese | English |
|---|---|---|
| Event_00_25 | おしえてイカロス先生 / DS本体を持ち替えて下さい (chalkboard; same art as DelusionSelect/Event_00_25_m) | Teach Me, Ikaros-sensei / Please turn your DS sideways |
| Event_00_29 | フィニッシュマーク | Finish Mark |
| Event_00_31 | タイムゲージ | Time Gauge |
| Event_00_32 | Results screen (same as Result_DownBG_Normal) | Results / Growth Points Earned / Time / Happenings Failed / Total Growth Points Earned |
| Event_00_35 | ハプニングタイム banner | Happening Time |
| Event_00_36 | ハプニング対処タイム | Happening Time Limit |
| Event_00_37 | タッチマーカー / スクラッチマーカー | Touch Marker / Scratch Marker |
| Event_00_38 / 39 | 成功！ / 失敗！ | Success! / Failure! |
| Event_00_40 | リトライ / タイトルに戻る / スキップする | Retry / Return to Title / Skip |
| Event_00_41 | タッチ / スライド | Touch / Slide |

## NormalMain

Bg_* are location backdrops (two rotated halves, like EventMain). Only Bg_30_000 has text: the pink 脳内☆補完中 banner
over black in delusion scenes -> "Delusion☆Mode".

## Friendly

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| Friendly | Friendly_BG | Intimacy screen | 親密度 | Intimacy | header tab |
| Friendly | Friendly_TEX00 | sprites | モドル | Back | |

## Help

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| Help | Help_Text00_00, _00_01, 01_00, 01_01, 02_00, 03_00 - 03_08, 04_00 - 04_04 (19 files) | help pages | brown-on-white help paragraphs, several lines per page | (unreadable until rendered) | garbled - needs proper render |
| Help | Help_Window01 - Help_Window04 (4 files) | help popup windows | pink window with title bar + body text | (unreadable) | garbled - needs proper render |
| Help | HelpList_TEX | help topic list buttons | button labels (unreadable) | | garbled - needs proper render |
| Help | Help_Common | common sprite strip | pink text fragments | | garbled - needs proper render (256x16) |

No text: Help_CommonBG. Already English: HelpList_BG ("HELP" header).

## Logo

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| Logo | LogoBG01 | publisher splash | 角川書店 (logo) | Kadokawa Shoten | corporate logo; probably keep as-is |

Already English: LicensedBy_GrayWhite, LogoBG02 (seventh chord), criware256x192sw.

## MainTitle

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| MainTitle | Title_Second_TEX00 | game logo | そらのおとしもの フォルテ / ドリーミーシーズン (under "Dreamy Season") | Heaven's Lost Property Forte / Dreamy Season | logo art + small katakana subtitle (x2 styles) |
| MainTitle | Title_Second_TEX01 | main menu buttons (blue) | はじめから / つづきから / トモ☆コレ / オプション / アルバム / フリーコミュニケーション / 部員名簿 / 戻る | New Game / Continue / Tomo☆Colle / Options / Album / Free Communication / Member Roster / Back | |
| MainTitle | Title_Second_TEX02 | main menu buttons (pink) | same 8 labels | same | selected-state copy of TEX01 |
| MainTitle | Title_Second_DownBG | copyright line | ©2010水無月すう/角川書店/新大陸発見部フォルテ ©角川書店 | ©2010 Suu Minazuki / Kadokawa Shoten / New World Discovery Club Forte ©Kadokawa Shoten | small text over sky |

No text: Title_First_UpWing00 - Title_First_UpWing07, Title_Second_UpBG, Title_Second_TEX03. Already English: Title_First_TEX00 ("written by SUU MINAZUKI").

## NormalSub

No text: SampleSub (starfield, slightly garbled).

## Option

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| Option | Option_Tex00 | options page 1 | ボリューム設定; メッセージ音; テキスト設定; 文章スキップ; 既読のみ / すべて (x2 styles); 設定1 | Volume Settings; Message Sound; Text Settings; Text Skip; Read Only / All; Settings 1 | OPTION, BGM, SE, VOICE, ON/OFF, typeA/B/C already English |
| Option | Option_Tex01 | options page 2 | ビジュアル設定; コミュニケーション画面; サイドキャラクター設定; 全てON / 全てOFF (x2); 設定2; モドル | Visual Settings; Communication Screen; Side Character Settings; All ON / All OFF; Settings 2; Back | |
| Option | Option_UpBG | top-screen bg | game logo, small (そらのおとしもの…) | (logo) | OBJ cells (NCER); renders fine as cells, see Game logo above |

No text: Option_DownBG.

## Result

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| Result | Result_DownBG_Normal | results panel | リザルト; 入手成長ポイント; タイム; ハプニング回避失敗; 合計入手成長ポイント | Results; Growth Points Earned; Time; Happenings Failed; Total Growth Points Earned | "Rank" already English |
| Result | Result_DownBG_Turn | results panel, rotated | same as _Normal, set vertically | same | rotated 90° for the sideways-DS layout |
| Result | Result_UpBG00 - Result_UpBG21 (22 files) | result banner over character art | コミュニケーション終了！ | Communication Over! | same text in all 22; 07, 10, 14, 15, 20 vertical |

Already English: Result_Interface_Normal, Result_Interface_Turn (NEW RECORD, digits, S/A/B/C/D, Rank).

## ShowTitle

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| ShowTitle | ShowTitle_Chapter00_TEX | episode title card | 第1話 服よさらば | Episode 1: Farewell, Clothes | |
| ShowTitle | ShowTitle_Chapter01_TEX | episode title card | 第2話 智樹先生ありがとう | Episode 2: Thank You, Tomoki-sensei | |
| ShowTitle | ShowTitle_Chapter02_TEX | episode title card | 第3話 こすれ、トモキ | Episode 3: Rub It, Tomoki | stale "がとう" tiles from ep.2 after the title (likely hidden) |
| ShowTitle | ShowTitle_Chapter03_TEX | episode title card | 第4話 煩悩は爆発だ！ | Episode 4: Lust Is an Explosion! | stale "がとう" tiles after title |
| ShowTitle | ShowTitle_Chapter04_TEX | episode title card | 第5話 妄想はどこまでも | Episode 5: Delusions Without End | |
| ShowTitle | ShowTitle_Chapter05_TEX | episode title card | 第6話 +1人いる！ | Episode 6: There's +1 Person! | stale "こまでも" tiles after title |
| ShowTitle | ShowTitle_Logo_TEX | game logo | そらのおとしもの フォルテ / ドリーミーシーズン | (logo) | same logo as Title_Second_TEX00 |

No text: ShowTitle_Chapter00_BG - ShowTitle_Chapter05_BG, ShowTitle_Logo_BG, ShowTitle_Logo_UpBG.

## StaffRoll

`StaffRoll_DownNN_MM`: NN = 00-06 is one variant per character/colour (Ikaros, Nymph, Astraea, Sohara, Mikako, Sugata, Tomoki/mixed); MM = 00-32 are strips that scroll as one long banner. **Credit text is identical in all 7 sets**, so each row below covers 7 files (Down00_MM ... Down06_MM). Text is blue-outlined labels in pink wing tags over art/photos. Names wrap across adjacent strips.

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| StaffRoll | StaffRoll_DownNN_00 | credits | そらのおとしもの フォルテ | Heaven's Lost Property Forte | "Dreamy Season" already English |
| StaffRoll | StaffRoll_DownNN_01 - _02 | credits | 原作 水無月すう（月刊「少年エース」連載 角川コミックス・エース刊）; キャスト | Original Work: Suu Minazuki (serialized in Monthly Shonen Ace, published by Kadokawa Comics Ace); Cast | |
| StaffRoll | StaffRoll_DownNN_02 - _04 | credits (cast) | イカロス 早見沙織 / 桜井智樹 保志総一朗 / 見月そはら 美名 / 守形英四郎 鈴木達央 / 五月田根美香子 高垣彩陽 / ニンフ 野水伊織 / アストレア 福原香織 / トモ子 藤田咲 | character + VA names | |
| StaffRoll | StaffRoll_DownNN_05 | credits | ゲーム開発 株式会社セブンスコード / 株式会社インフォ・スパイシー | Game Development: Seventh Chord Inc. / Info Spicy Inc. | |
| StaffRoll | StaffRoll_DownNN_06 - _08 | credits | ディレクション＆ゲームデザイン 下会所盛彦; メインプランナー 鈴木啓; コミュニケーションモードプランナー | Direction & Game Design; Main Planner; Communication Mode Planner | |
| StaffRoll | StaffRoll_DownNN_09 - _11 | credits | (CM planners) 鈴木啓 広瀬政和 辻井真矢 清水康吏; シナリオプロデュース 重馬敬（シナリオ工房 月光）; シナリオ 井草薫 むらさきゆきや あさりまみれ 秋月ひろ（ランアンドガン） 持田康之; スペシャルサンクス 柿原優子（シナリオ工房 月光） | Scenario Producer; Scenario; Special Thanks | |
| StaffRoll | StaffRoll_DownNN_12 - _14 | credits | スクリプター 広瀬政和 辻井真矢; メインプログラマー 東谷勇人; プログラマー 小山和光; チーフデザイナー 飛鳥馬恒; デザイナー | Scripters; Main Programmer; Programmer; Chief Designer; Designers | |
| StaffRoll | StaffRoll_DownNN_15 - _17 | credits | (designers) 戸谷大輔 宗雅 遠藤健史 小島千昌 廣谷香機 佐藤裕幸 野原康太郎; フォントワークス株式会社; サウンド 皆月一; ディレクション＆プランニングサポート 青木恭美 | Designers; Fontworks Inc.; Sound; Direction & Planning Support | |
| StaffRoll | StaffRoll_DownNN_18 - _20 | credits | プロダクトマネージャー 小満幸一; 音響制作 グロービジョン株式会社 (+5 names: 伊藤映里 宮薗直子 黒崎裕樹 吉岡拓真 郡司哲也); 音響制作協力 整音スタジオ 加藤恵美（整音スタジオ） | Product Manager; Sound Production: Glovision Inc.; Sound Production Assistance: Seion Studio | names transcribed from small text, verify |
| StaffRoll | StaffRoll_DownNN_21 - _23 | credits | 開発プロデューサー 中越昌宏（インフォ・スパイシー）; 取扱説明書 パッケージデザイン スタジオWOW!; WEB制作 角川デジックス; 協力 | Development Producer; Manual & Package Design: Studio WOW!; Web: Kadokawa Digix; Special Cooperation | |
| StaffRoll | StaffRoll_DownNN_24 - _25 | credits | 松宮園典（角川書店／少年エース編集部）/ 蜂屋誠一・西山洋介・小倉理恵・倉兼千晶（角川書店／アニメーション部）/ AIC ASTA | Kadokawa Shoten / Shonen Ace editorial dept.; Animation dept. | |
| StaffRoll | StaffRoll_DownNN_26 - _29 | credits | 製作／制作 株式会社角川書店; プロデューサー 山下雅水; 広報 麟太; シニアプロデューサー 藤岡迅彦; エグゼクティブプロデューサー 安田猛; 制作総指揮 井上伸一郎 | Production: Kadokawa Shoten; Producer; PR; Senior Producer; Executive Producer; Executive in Charge of Production | |
| StaffRoll | StaffRoll_DownNN_30 | credits | ©2010 水無月すう／角川書店／新大陸発見部フォルテ ©角川書店 | ©2010 Suu Minazuki / Kadokawa Shoten / New World Discovery Club Forte ©Kadokawa Shoten | |
| StaffRoll | StaffRoll_DownNN_31 | credits | 角川書店 (logo) | Kadokawa Shoten | corporate logo; probably keep |
| StaffRoll | StaffComplete_Down | all-clear screen | オールクリアおめでとうございます。 | Congratulations on clearing everything! | text over chibi cast art |
| StaffRoll | StaffFin_Up | end logo | そらのおとしもの フォルテ / ドリーミーシーズン | (logo) | |
| StaffRoll | StaffRoll_Up | credits top-screen logo | そらのおとしもの フォルテ / ドリーミーシーズン | (logo) | |

No text: StaffRoll_Down00_32 - StaffRoll_Down06_32 (blank end strips). Already English: StaffFin_Down00 - StaffFin_Down06 ("fin").

**Unverified staff-name readings** (best guesses from the kanji; correct them when a source turns up): 下会所盛彦 Morihiko Shimogaisho; 鈴木啓 Kei Suzuki; 辻井真矢 Shinya Tsujii (could be Maya); 清水康吏 Yasushi Shimizu (2nd kanji could be 更); 東谷勇人 Hayato Higashitani; 小山和光 Kazumitsu Koyama; 飛鳥馬恒 Hisashi Asuma; 戸谷大輔 Daisuke Toya; 宗雅 Masashi So; 遠藤健史 Takeshi Endo; 小島千昌 Chiaki Kojima; 廣谷香機 Koki Hiroya; 皆月一 Hajime Minazuki; 青木恭美 Kyomi Aoki; 小満幸一 Koichi Komitsu; 黒崎裕樹 Hiroki Kurosaki; 加藤恵美 Emi Kato; 中越昌宏 Masahiro Nakagoshi; 倉兼千晶 Chiaki Kuragane; 山下雅水 Masami Yamashita; 藤岡迅彦 Toshihiko Fujioka. Also worth a check: あさりまみれ Mamire Asari (pen name, split guessed); 重馬敬 Kei Shigema; 麟太 Rinta; 松宮廣典 Hironori Matsumiya (image shows 廣典, not 園典). The StaffRoll specs are generated by a scratch script (layout + per-variant offset matching); to change a name, edit all 7 variants' text ops for that strip.

## TomokiMonitor

All 70 are garbled (grey, no palette, scrambled tiles) and need a proper render. Text shapes are visible in most of them.

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| TomokiMonitor | Monitor_Emblem00 - Monitor_Emblem19 (20 files) | title (称号) name strips | kanji/kana strips (unreadable) | (title names) | garbled; probably the same 20 titles as the Load/Save sets |
| TomokiMonitor | Monitor_Load_Emblem00 - _19, Monitor_Save_Emblem00 - _19 (40 files) | title name strips on the load/save screens | kanji/kana strips (unreadable) | (title names) | garbled; Load_ and Save_ look pixel-identical |
| TomokiMonitor | Monitor_FCLoad_Telop | caption/telop text | fragments: …ミュニケーション, …ています。, …を行います | (load caption) | garbled (rows misaligned), 512x192 |
| TomokiMonitor | Monitor_BG00, Monitor_BG01, Monitor_Load_BG00, Monitor_Load_BG01, Monitor_Save_BG00, Monitor_Save_BG01 | Tomoki Monitor / load / save screen bgs | label boxes with text (unreadable) | | garbled |
| TomokiMonitor | Monitor_Misc, Monitor_Load_Misc, Monitor_Save_Misc | sprite sheets | digits + possible labels (unreadable) | | garbled |

## TomokiTraining

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| TomokiTraining | Training_DownBG | Tomoki☆Training screen | 智樹☆トレーニング; 成長ポイント; 消費ポイント | Tomoki☆Training; Growth Points; Points Cost | LV /10 already English |
| TomokiTraining | Training_DownTEX00 | stat wheel sprites | 煩悩耐久力 / 指先技術力 / 変態紳士力 / 生存本能力 / 異性懐柔力; ⓧ妄想コミュニケーションへ (x2); モドル | Lust Endurance / Finger Technique / Pervert Gentleman / Survival Instinct / Charm; To Delusion Communication; Back | LV MAX already English |
| TomokiTraining | Training_DownTEX01 | dialog parts | はい x3 / いいえ x3; このパラメータを成長させますか？ / 成長ポイントが足りません。 | Yes / No; Raise this stat? / Not enough Growth Points. | |
| TomokiTraining | Training_DownTEX02 | stat hint banners (6) | コミュニケーション中のタイムが増えるぞ！ / 上げまくってじっくり楽しもうぜ！ / フィーリング値が溜まりやすくなるぞ！ / でもハプニングが起きやすくなるから注意してくれよな！ / フィーリング値の減少を抑え、ハプニングが起こりにくくなるぞ！ / 落ち着いた紳士の魅力にあの子もイチコロさ！ | More time during Communication! / Max it out and take your sweet time! / Feeling fills up faster! / But Happenings get more likely, so watch out! / Feeling drains slower and Happenings get rarer! / She'll fall for a cool gentleman's charm in no time! | pink boxes, 1-2 lines each |
| TomokiTraining | Training_DownTEX03 | stat hint banners (4) | ハプニングに対応できる時間が延びるぞ！ / どんなピンチだってくぐり抜けてみせるぜ！ / 相手の機嫌を損ねにくくなり、連続的なアタックが可能になるぞ！ / 円滑なコミュニケーションを心がけようぜ！ | More time to react to Happenings! / I'll get through any pinch! / She's harder to upset, so you can chain attacks! / Keep the communication smooth! | |

Garbled, no text visible (grey, no palette; needs proper render to confirm): Training_UpAnime00 - Training_UpAnime04, Training_UpBG00 - Training_UpBG04.

## Trial_TrialInterface

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| Trial_TrialInterface | Trial_Common_Interface | Communication HUD sprites | ハプニングタイム (logo) | Happening Time | stylised logo; rest is icons/digits |
| Trial_TrialInterface | Trial_Various_Counter | result popups | 成功！ / 失敗！ | Success! / Failure! | between wing graphics |
| Trial_TrialInterface | Trial_Various_GameOver | Game Over menu | リトライ / タイトルに戻る / スキップする (each as button + plain text) | Retry / Return to Title / Skip | "GAME OVER" already English |
| Trial_TrialInterface | Trial_Various_Pause | pause menu | 煩悩耐久力 / 指先技術力 / 変態紳士力 / 生存本能力 / 異性懐柔力; はい / いいえ (x2 styles); スキップしますか？ | stat labels; Yes / No; Skip? | "-PAUSE-", LV already English |

No text: Trial_Various_Talk00, Trial_Various_Talk01.

## Wallpaper

**This folder looks like leftover assets from another Kadokawa/Seventh Chord DS title (Strike Witches): "STRIKE WITCHES" logo, Witch registration cards with English names (Mio Sakamoto, etc.).** Check whether the game uses it before translating anything here. Most files are garbled.

| folder | file | what it is | Japanese | English | notes |
|---|---|---|---|---|---|
| Wallpaper | down_bg | wallpaper menu header | カベガミ | Wallpaper | clean render |
| Wallpaper | up_bg00 | controls guide | fragments: ボタン, オートモード?, メッセージ?, ウインドウ, 操作, 指南, ON/OFF, START, SELECT | button controls guide | garbled - needs proper render |
| Wallpaper | up_bg01, up_bg02 | Strike Witches logo screen | ストライクウィッチーズ (big katakana logo) | Strike Witches | garbled; logo, probably not ours |
| Wallpaper | etc | sprite sheet | unknown | | garbled; may contain text |

Already English (garbled): up_bg03 - up_bg16 (character registration cards: "STRIKE WITCHES", "register of members", romanised names), up_bg17 ("No Data").
