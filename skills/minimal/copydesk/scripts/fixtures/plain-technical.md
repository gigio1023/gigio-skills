# Plain technical prose

Plain sentences written for this fixture. `check_slop.py` should report few or no hits here; a hit is a false positive to read, not a defect in the text.

## Cache invalidation

The build cache is keyed by the lockfile hash and the compiler version. When either changes, the next build starts cold and takes about four minutes on a CI runner. We keep the key narrow on purpose: adding the full environment made cache hits rare because unrelated variables changed on every run.

The cache server returns 404 for a missing key and 503 when it is overloaded. The client treats 404 as a miss and 503 as a reason to build without the cache, so an outage slows builds but never fails them.

- The cache holds the last 20 builds per branch.
- Entries older than 14 days are removed by a nightly job.
- A manual purge needs the `cache-admin` role.

## Judge agreement

We compared the judge prediction with the human reference label on 400 items. The judge agreed on 352 of them, and most disagreements came from answers that cited the right policy but quoted an outdated version. Raising the temperature from 0 to 0.7 lowered agreement to 331, so the release keeps temperature 0.

## 캐시 무효화

빌드 cache key는 lockfile hash와 compiler version으로 만든다. 둘 중 하나가 바뀌면 다음 빌드는 cache 없이 시작하고 CI runner에서 약 4분이 걸린다. 전체 환경 변수를 key에 넣었을 때는 무관한 값이 매번 바뀌어 cache hit가 거의 나오지 않았다.

cache server가 404를 돌려주면 client는 miss로 처리한다. 503은 서버 과부하이므로 cache 없이 빌드한다. 장애가 나도 빌드는 느려질 뿐 실패하지 않는다. 실패한 빌드는 runner log, 설정 화면, 재현 명령을 함께 남긴다.

## Judge 일치도

400개 항목에서 judge prediction과 human reference label을 비교했다. 352개가 일치했고 불일치는 대부분 정책을 맞게 인용했지만 옛 판본을 근거로 든 답변에서 나왔다. temperature를 0에서 0.7로 올리면 일치 항목이 331개로 줄어서 배포 설정은 0으로 둔다.

| Setting | Agreement |
| --- | --- |
| temperature 0 | 352 / 400 |
| temperature 0.7 | 331 / 400 |
