RAG pipeline - animated explainer reel (Fri 16 Oct 2026, 7:00 PM IST) - scene assets

Canvas: 1080x1920. Every layer is a full-canvas transparent PNG, already in position; stack them over bg.png in the order listed.
Bottom 20% (y > 1536) is empty in every layer. bg.png = dark background + panel only. composite.png = bg + all layers (preview).
Fonts: Archivo Black, Poppins, IBM Plex Mono. Accent #FFC800. Icons are hand-drawn vectors (PIL), no stock or logos.
Generator: generate.py (python3 generate.py <outdir>). Contact sheet: contact-sheet.png. Cover: cover.jpg.
Raw URL pattern: https://raw.githubusercontent.com/Shiv907/instagram-carousel-assets/main/reels/2026/10/2026-10-16-rag-pipeline-animated/sceneN/<file>.png

scene1/  Hook - "Aapke PDFs se answer kaise?"
  bg.png (background)
  01-icon-chatbot.png   bbox (252, 435, 767, 1041)
  02-icon-pdf.png   bbox (664, 675, 858, 906)
  03-text-hook.png   bbox (160, 1164, 919, 1364)
  composite.png (preview, not a layer)

scene2/  Title - "RAG = Retrieval Augmented Generation"
  bg.png (background)
  01-text-rag-equals.png   bbox (291, 392, 792, 513)
  02-text-retrieval.png   bbox (284, 689, 796, 779)
  03-text-augmented.png   bbox (210, 909, 865, 1020)
  04-text-generation.png   bbox (222, 1129, 857, 1219)
  composite.png (preview, not a layer)

scene3/  Prep stage - Documents -> Chunks -> Embeddings [0.12, -0.4, ...] (illustrative) -> Vector DB
  bg.png (background)
  01-box-documents.png   bbox (110, 340, 971, 541)
  02-arrow-1.png   bbox (522, 554, 558, 627)
  03-box-chunks.png   bbox (110, 640, 971, 841)
  04-arrow-2.png   bbox (522, 854, 558, 927)
  05-box-embeddings.png   bbox (110, 940, 971, 1141)
  06-arrow-3.png   bbox (522, 1154, 558, 1227)
  07-box-vector-db.png   bbox (110, 1240, 971, 1441)
  composite.png (preview, not a layer)

scene4/  Query stage - "Retrieval": User question -> Embedding -> Search in Vector DB -> Top chunks returned
  bg.png (background)
  01-label-retrieval.png   bbox (296, 323, 786, 411)
  02-box-user-question.png   bbox (110, 490, 971, 661)
  03-arrow-1.png   bbox (522, 672, 558, 734)
  04-box-embedding.png   bbox (110, 745, 971, 916)
  05-arrow-2.png   bbox (522, 927, 558, 989)
  06-box-search-in-vector-db.png   bbox (110, 1000, 971, 1171)
  07-arrow-3.png   bbox (522, 1182, 558, 1244)
  08-box-top-chunks-returned.png   bbox (110, 1255, 971, 1426)
  composite.png (preview, not a layer)

scene5/  "Generation": Chunks + Question -> LLM -> Answer
  bg.png (background)
  01-label-generation.png   bbox (234, 323, 844, 411)
  02-box-chunks.png   bbox (110, 500, 491, 701)
  03-plus.png   bbox (510, 554, 571, 614)
  04-box-question.png   bbox (590, 500, 971, 701)
  05-arrows-to-llm.png   bbox (293, 708, 789, 851)
  06-box-llm.png   bbox (110, 870, 971, 1081)
  07-arrow-to-answer.png   bbox (522, 1095, 558, 1206)
  08-box-answer.png   bbox (110, 1220, 971, 1421)
  composite.png (preview, not a layer)

scene6/  AWS - "Amazon Bedrock Knowledge Bases = ye sab managed" (plain text, no AWS logo)
  bg.png (background)
  01-box-bedrock-kb.png   bbox (110, 420, 971, 821)
  02-equals.png   bbox (498, 873, 582, 933)
  03-text-ye-sab-managed.png   bbox (124, 1073, 951, 1173)
  04-icons-pipeline-managed.png   bbox (214, 1240, 816, 1375)
  composite.png (preview, not a layer)

scene7/  CTA - "Next: Embeddings | Follow + Save" + @shivanshu_builds (the "|" is its own layer, 02-divider, between the two cards)
  bg.png (background)
  01-card-next-embeddings.png   bbox (110, 420, 971, 641)
  02-divider.png   bbox (534, 690, 547, 775)
  03-card-follow-save.png   bbox (110, 850, 971, 1071)
  04-handle.png   bbox (207, 1196, 876, 1269)
  composite.png (preview, not a layer)

